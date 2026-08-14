import React, { useState, useEffect } from 'react';
import Header from '../components/layout/Header';
import Sidebar from '../components/layout/Sidebar';
import ChatWindow from '../components/chat/ChatWindow';
import ChatInput from '../components/chat/ChatInput';
import SettingsModal from '../components/modals/SettingsModal';
import { useOnlineStatus } from '../hooks/useOnlineStatus';
import { performOfflineSearch } from '../utils/offlineSearch';
import { sendMessage, fetchChatSessions, fetchChatSession, deleteChatSession, clearAllChatSessions } from '../services/chatApi';

const ChatPage = () => {
  const isOnline = useOnlineStatus();
  const [language, setLanguage] = useState('en');
  const [sessions, setSessions] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentMode, setCurrentMode] = useState('online');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(() => {
    try {
      const stored = localStorage.getItem('cambodia_ai_sidebar_collapsed');
      return stored !== null ? JSON.parse(stored) : false;
    } catch (e) {
      return false;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem('cambodia_ai_sidebar_collapsed', JSON.stringify(isSidebarCollapsed));
    } catch (e) {}
  }, [isSidebarCollapsed]);

  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  
  // User Profile state with localStorage persistence
  const [userProfile, setUserProfile] = useState(() => {
    try {
      const stored = localStorage.getItem('cambodia_ai_user_profile');
      return stored ? JSON.parse(stored) : { name: 'Traveler', email: '', travelStyle: 'cultural', preferredDestinations: ['siem_reap'] };
    } catch (e) {
      return { name: 'Traveler', email: '', travelStyle: 'cultural', preferredDestinations: ['siem_reap'] };
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem('cambodia_ai_user_profile', JSON.stringify(userProfile));
    } catch (e) {}
  }, [userProfile]);

  // Update current mode state when network changes
  useEffect(() => {
    if (!isOnline) {
      setCurrentMode('offline');
    } else {
      setCurrentMode('online');
    }
  }, [isOnline]);

  // Load chat sessions and restore active conversation on refresh/load
  useEffect(() => {
    let isMounted = true;

    const initChat = async () => {
      // 1. Immediately load local cache for zero-flicker UI
      const localList = loadLocalSessions();
      
      const lastSessionId = localStorage.getItem('aichat_last_active_session_id');
      if (lastSessionId) {
        handleSelectSession(lastSessionId);
      }

      // 2. Sync online sessions seamlessly
      if (isOnline) {
        try {
          const data = await fetchChatSessions();
          if (isMounted && data && Array.isArray(data)) {
            setSessions(data);
          }
        } catch (err) {
          console.warn('Online sessions sync note:', err);
        }
      }
    };

    initChat();
    return () => { isMounted = false; };
  }, [isOnline]);

  const loadSessions = async () => {
    try {
      const data = await fetchChatSessions();
      const sessionList = data || [];
      setSessions(sessionList);
      return sessionList;
    } catch (err) {
      console.warn('Could not fetch online sessions. Falling back to local sessions storage:', err);
      return loadLocalSessions();
    }
  };

  const loadLocalSessions = () => {
    try {
      const stored = localStorage.getItem('aichat_local_sessions');
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed)) {
          setSessions(parsed);
          return parsed;
        }
      }
    } catch (e) {
      console.error('Error reading local sessions from localStorage:', e);
    }
    return [];
  };

  const saveLocalSession = (newSession) => {
    try {
      const stored = localStorage.getItem('aichat_local_sessions');
      let localSessions = stored ? JSON.parse(stored) : [];
      if (!Array.isArray(localSessions)) localSessions = [];
      const idx = localSessions.findIndex((s) => s.session_id === newSession.session_id);
      if (idx >= 0) {
        localSessions[idx] = newSession;
      } else {
        localSessions.unshift(newSession);
      }
      localStorage.setItem('aichat_local_sessions', JSON.stringify(localSessions));
      setSessions(localSessions);
    } catch (e) {
      console.error('Error saving local session:', e);
    }
  };

  // Switch chat session
  const handleSelectSession = async (sessionId) => {
    if (!sessionId) return;
    setCurrentSessionId(sessionId);
    localStorage.setItem('aichat_last_active_session_id', sessionId);
    setError(null);

    // 1. Try server fetch if online
    if (isOnline) {
      try {
        const data = await fetchChatSession(sessionId);
        const resData = (data && data.data) ? data.data : data;
        if (resData && resData.messages && Array.isArray(resData.messages) && resData.messages.length > 0) {
          const formattedMsgs = resData.messages.map((m, idx) => ({
            id: m.id || (idx + 1),
            sender: m.sender || (m.role === 'assistant' ? 'ai' : m.role || 'user'),
            message: m.message || m.content || '',
            mode: m.mode || 'online',
            created_at: m.created_at || new Date().toISOString()
          }));
          setMessages(formattedMsgs);
          if (resData.metadata && resData.metadata.language) {
            setLanguage(resData.metadata.language);
          }
          return;
        }
      } catch (err) {
        console.warn('Online session fetch failed, checking local sessions:', err);
      }
    }

    // 2. Fallback to localStorage sessions
    try {
      const stored = localStorage.getItem('aichat_local_sessions');
      const localList = stored ? JSON.parse(stored) : [];
      const local = Array.isArray(localList) ? localList.find((s) => s.session_id === sessionId) : null;
      if (local && local.messages && Array.isArray(local.messages)) {
        const formattedMsgs = local.messages.map((m, idx) => ({
          id: m.id || (idx + 1),
          sender: m.sender || (m.role === 'assistant' ? 'ai' : m.role || 'user'),
          message: m.message || m.content || '',
          mode: m.mode || 'offline',
          created_at: m.created_at || new Date().toISOString()
        }));
        setMessages(formattedMsgs);
        if (local.language) {
          setLanguage(local.language);
        }
      }
    } catch (e) {
      console.error('Error reading local session backup:', e);
    }
  };

  // Create New Chat
  const handleNewChat = () => {
    setCurrentSessionId(null);
    localStorage.removeItem('aichat_last_active_session_id');
    setMessages([]);
    setError(null);
  };

  // Clear / Delete all chat history
  const handleClearChat = async () => {
    if (isOnline) {
      try {
        await clearAllChatSessions();
      } catch (err) {
        console.warn('Error clearing sessions on server:', err);
      }
    }
    try {
      localStorage.removeItem('aichat_local_sessions');
      localStorage.removeItem('aichat_last_active_session_id');
    } catch (e) {
      console.error('Error clearing local session storage:', e);
    }
    setSessions([]);
    handleNewChat();
  };

  // Delete single session
  const handleDeleteSession = async (sessionId) => {
    if (isOnline) {
      try {
        await deleteChatSession(sessionId);
        await loadSessions();
      } catch (err) {
        console.warn('Error deleting session on server:', err);
      }
    }
    try {
      const stored = localStorage.getItem('aichat_local_sessions');
      if (stored) {
        let localSessions = JSON.parse(stored);
        localSessions = localSessions.filter((s) => s.session_id !== sessionId);
        localStorage.setItem('aichat_local_sessions', JSON.stringify(localSessions));
      }
    } catch (e) {
      console.error('Error updating local sessions:', e);
    }
    setSessions((prev) => (Array.isArray(prev) ? prev.filter((s) => s.session_id !== sessionId) : []));
    if (currentSessionId === sessionId) {
      handleNewChat();
    }
  };

  // Send Message Handler
  const handleSendMessage = async (text, attachments = []) => {
    if (!text || !text.trim() || isLoading) return;

    setError(null);
    const userMessageText = text.trim();

    // Optimistically append user message to UI
    const tempUserMsg = {
      id: Date.now(),
      sender: 'user',
      message: userMessageText,
      attachments: attachments,
      created_at: new Date().toISOString()
    };

    setMessages((prev) => [...prev, tempUserMsg]);
    setIsLoading(true);

    try {
      let aiMsg = null;
      let respMode = 'offline';
      let activeSid = currentSessionId;

      // 1. Try sending message to FastAPI backend
      try {
        const response = await sendMessage({
          message: userMessageText,
          language: language,
          session_id: currentSessionId
        });

        const apiPayload = response?.data?.data ?? response?.data ?? response;

        if (response && (response.success || apiPayload)) {
          const sid = apiPayload?.session_id || currentSessionId || `session_${Date.now()}`;
          if (sid) {
            activeSid = sid;
            setCurrentSessionId(sid);
            localStorage.setItem('aichat_last_active_session_id', sid);
          }

          respMode = apiPayload?.mode || (isOnline ? 'online' : 'offline');
          setCurrentMode(respMode);

          aiMsg = {
            id: Date.now() + 1,
            sender: 'ai',
            message: apiPayload?.answer || apiPayload?.message || 'No response text available.',
            mode: respMode,
            intent: apiPayload?.intent,
            analysis: apiPayload?.analysis,
            summary: apiPayload?.summary,
            sentiment: apiPayload?.sentiment,
            sources: apiPayload?.sources || [],
            suggestions: apiPayload?.suggestions || [],
            created_at: new Date().toISOString()
          };

          if (isOnline) loadSessions();
        }
      } catch (err) {
        console.warn('Backend API call unreached. Switching to client-side offline search:', err);
      }

      // 2. Client-side search fallback if backend unreachable
      if (!aiMsg) {
        const offlineRes = await performOfflineSearch(userMessageText, language);
        activeSid = activeSid || `off_${Date.now()}`;
        setCurrentSessionId(activeSid);
        localStorage.setItem('aichat_last_active_session_id', activeSid);

        aiMsg = {
          id: Date.now() + 1,
          sender: 'ai',
          message: offlineRes.message,
          mode: 'offline',
          sources: offlineRes.sources || [],
          created_at: new Date().toISOString()
        };
        setCurrentMode('offline');
      }

      // Append AI response
      if (aiMsg && activeSid) {
        localStorage.setItem('aichat_last_active_session_id', activeSid);
        setMessages((prev) => {
          const updated = [...prev, aiMsg];
          const firstUserMsg = updated.find(m => m.sender === 'user' || m.role === 'user');
          const cleanTitle = firstUserMsg ? firstUserMsg.message : userMessageText;

          saveLocalSession({
            session_id: activeSid,
            title: cleanTitle,
            language: language,
            created_at: new Date().toISOString(),
            messages: updated
          });
          return updated;
        });
      }

    } catch (e) {
      console.error('Error in chat handler:', e);
      setError('Failed to process message.');
    } finally {
      setIsLoading(false);
    }
  };

  // Regenerate last AI response
  const handleRegenerate = async () => {
    if (messages.length === 0 || isLoading) return;
    const lastUserMsg = [...messages].reverse().find((m) => m.sender === 'user' || m.role === 'user');
    if (lastUserMsg && lastUserMsg.message) {
      handleSendMessage(lastUserMsg.message);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#f8fafc] dark:bg-[#18181b] text-slate-900 dark:text-slate-100 transition-colors duration-200 overflow-hidden font-sans">
      
      {/* Header */}
      <Header
        language={language}
        setLanguage={setLanguage}
        isMobileMenuOpen={isMobileMenuOpen}
        setIsMobileMenuOpen={setIsMobileMenuOpen}
        isOnline={isOnline}
        mode={currentMode}
        onOpenSettings={() => setIsSettingsOpen(true)}
        isSidebarCollapsed={isSidebarCollapsed}
        onToggleSidebarCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
      />

      {/* Main Container */}
      <div className="flex flex-1 overflow-hidden relative">
        {/* Left Sidebar */}
        <Sidebar
          sessions={sessions}
          currentSessionId={currentSessionId}
          onSelectSession={handleSelectSession}
          onNewChat={handleNewChat}
          onClearChat={handleClearChat}
          onDeleteSession={handleDeleteSession}
          onQuickQuery={handleSendMessage}
          language={language}
          isOpen={isMobileMenuOpen}
          setIsOpen={setIsMobileMenuOpen}
          isCollapsed={isSidebarCollapsed}
          setIsCollapsed={setIsSidebarCollapsed}
          onOpenSettings={() => setIsSettingsOpen(true)}
          userProfile={userProfile}
        />

        {/* Chat Window & Input Area */}
        <main className="flex-1 flex flex-col h-full min-w-0">
          <ChatWindow
            messages={messages}
            isLoading={isLoading}
            error={error}
            onSendMessage={handleSendMessage}
            onRegenerate={handleRegenerate}
            language={language}
          />
          <ChatInput
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            language={language}
          />
        </main>
      </div>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        language={language}
        setLanguage={setLanguage}
        userProfile={userProfile}
        setUserProfile={setUserProfile}
      />
    </div>
  );
};

export default ChatPage;
