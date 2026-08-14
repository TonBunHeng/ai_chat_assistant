import React, { useState } from 'react';
import { 
  Plus, MessageSquare, Trash2, MapPin, Hotel, Utensils, Calendar, 
  ChevronRight, Sparkles, Search, Settings, User, X, AlertTriangle, 
  Compass, PanelLeftClose, PanelLeftOpen
} from 'lucide-react';

const Sidebar = ({
  sessions = [],
  currentSessionId,
  onSelectSession,
  onNewChat,
  onClearChat,
  onDeleteSession,
  onQuickQuery,
  language = 'en',
  isOpen,
  setIsOpen,
  isCollapsed,
  setIsCollapsed,
  onOpenSettings,
  userProfile = {}
}) => {
  const isKhmer = language === 'km';
  const [searchTerm, setSearchTerm] = useState('');

  // Delete modal state
  const [deleteModal, setDeleteModal] = useState({
    isOpen: false,
    deleteScope: 'ONE',
    selectedSessionId: ''
  });

  const openDeleteModal = (targetId = null) => {
    const initialId = targetId || currentSessionId || (sessions[0]?.session_id || '');
    setDeleteModal({
      isOpen: true,
      deleteScope: 'ONE',
      selectedSessionId: initialId
    });
  };

  const openDeleteSingleModal = (e, sessionId) => {
    e.stopPropagation();
    openDeleteModal(sessionId);
  };

  const handleConfirmDelete = () => {
    if (deleteModal.deleteScope === 'ALL') {
      if (onClearChat) onClearChat();
    } else if (deleteModal.deleteScope === 'ONE') {
      const targetId = deleteModal.selectedSessionId || currentSessionId || (sessions[0]?.session_id || '');
      if (targetId && onDeleteSession) {
        onDeleteSession(targetId);
      } else if (onClearChat) {
        onClearChat();
      }
    }
    setDeleteModal({ isOpen: false, deleteScope: 'ONE', selectedSessionId: '' });
  };

  // Filter sessions by search term
  const filteredSessions = Array.isArray(sessions)
    ? sessions.filter((sess) => {
        if (!sess) return false;
        if (!searchTerm.trim()) return true;
        const q = searchTerm.toLowerCase();
        const title = sess.title || '';
        const msgMatch = sess.messages && sess.messages.some(m => (m.message || m.content || '').toLowerCase().includes(q));
        return title.toLowerCase().includes(q) || msgMatch;
      })
    : [];

  return (
    <>
      {/* Mobile Overlay Backdrop */}
      {isOpen && (
        <div
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs z-40 md:hidden transition-opacity"
        />
      )}

      {/* Sidebar Main Element */}
      <aside
        className={`fixed md:static inset-y-0 left-0 z-40 bg-white dark:bg-[#18181b] border-r border-[#f3f4f6] dark:border-[#27272a] flex flex-col transition-[width,transform] duration-300 ease-in-out overflow-hidden ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        } ${
          isCollapsed ? 'md:w-20' : 'md:w-72'
        } w-72`}
      >
        {/* Top Header / New Chat */}
        <div className="p-3 border-b border-[#f3f4f6] dark:border-[#27272a] flex items-center justify-center">
          {/* New Chat Button */}
          <button
            onClick={() => {
              onNewChat();
              setIsOpen(false);
            }}
            className={`flex items-center justify-center bg-[#003E83] hover:bg-[#002e62] text-white font-medium py-3 rounded-2xl shadow-sm transition-all duration-300 ease-in-out active:scale-[0.99] cursor-pointer ${
              isCollapsed ? 'w-full px-0' : 'w-full px-4'
            }`}
            title={isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat'}
          >
            <Plus size={20} className="shrink-0" />
            <span
              className={`text-xs font-semibold whitespace-nowrap overflow-hidden transition-all duration-300 ease-in-out ${
                isCollapsed ? 'max-w-0 opacity-0 ml-0' : 'max-w-[160px] opacity-100 ml-2'
              }`}
            >
              {isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat'}
            </span>
          </button>
        </div>

        {/* Chat History List */}
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          <div
            className={`flex items-center justify-between px-2 py-1 overflow-hidden transition-all duration-300 ease-in-out ${
              isCollapsed ? 'max-h-0 opacity-0 py-0' : 'max-h-10 opacity-100'
            }`}
          >
            <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 dark:text-[#a1a1aa] whitespace-nowrap">
              {isKhmer ? 'ប្រវត្តិសន្ទនា' : 'Recent Chats'}
            </span>
            {sessions.length > 0 && (
              <button
                onClick={() => openDeleteModal()}
                className="text-[11px] text-rose-500 hover:text-rose-600 dark:hover:text-rose-400 font-medium transition-colors whitespace-nowrap cursor-pointer"
              >
                {isKhmer ? 'លុបទាំងអស់' : 'Clear All'}
              </button>
            )}
          </div>

          {filteredSessions.length === 0 ? (
            <div className="text-center py-8 px-2">
              <MessageSquare size={24} className="mx-auto text-slate-300 dark:text-slate-600 mb-2" />
              <p
                className={`text-xs text-slate-400 dark:text-slate-500 overflow-hidden transition-all duration-300 ease-in-out ${
                  isCollapsed ? 'max-h-0 opacity-0' : 'max-h-20 opacity-100'
                }`}
              >
                {searchTerm
                  ? (isKhmer ? 'រកមិនឃើញប្រវត្តិសន្ទនា' : 'No matching chats')
                  : (isKhmer ? 'មិនទាន់មានប្រវត្តិសន្ទនានៅឡើយទេ' : 'No recent chats yet')}
              </p>
            </div>
          ) : (
            filteredSessions.map((sess, idx) => {
              if (!sess) return null;
              const sid = sess.session_id || `sess_${idx}`;
              const isActive = sid === currentSessionId;
              
              let rawTitle = sess.title;
              if (!rawTitle || rawTitle.startsWith('Chat Session #')) {
                if (sess.messages && sess.messages.length > 0) {
                  const firstUserMsg = sess.messages.find(m => m.sender === 'user' || m.role === 'user');
                  rawTitle = firstUserMsg ? (firstUserMsg.message || firstUserMsg.content) : (sess.messages[0].message || sess.messages[0].content);
                }
              }
              
              const displayTitle = (rawTitle && !rawTitle.startsWith('Chat Session #'))
                ? rawTitle.trim()
                : (isKhmer ? 'ការសន្ទនាថ្មី' : 'New Chat');

              return (
                <div
                  key={sid}
                  onClick={() => {
                    if (sess.session_id) onSelectSession(sess.session_id);
                    setIsOpen(false);
                  }}
                  className={`group relative flex items-center p-2.5 rounded-xl cursor-pointer text-xs transition-all duration-300 ease-in-out ${
                    isCollapsed ? 'justify-center px-0' : 'justify-between px-2.5'
                  } ${
                    isActive
                      ? 'bg-[#003E83]/10 text-[#003E83] dark:text-[#60a5fa] font-semibold border border-[#003E83]/30'
                      : 'text-[#111827] dark:text-[#f4f4f5] hover:bg-[#f9fafb] dark:hover:bg-[#27272a]'
                  }`}
                  title={displayTitle}
                >
                  <div className="flex items-center min-w-0">
                    <MessageSquare size={16} className={`shrink-0 transition-all duration-300 ${isActive ? 'text-[#003E83] dark:text-[#60a5fa]' : 'text-[#6b7280] dark:text-[#a1a1aa]'}`} />
                    <span
                      className={`truncate whitespace-nowrap overflow-hidden transition-all duration-300 ease-in-out ${
                        isCollapsed ? 'max-w-0 opacity-0 ml-0' : 'max-w-[170px] opacity-100 ml-2.5'
                      }`}
                    >
                      {displayTitle}
                    </span>
                  </div>

                  <button
                    onClick={(e) => openDeleteSingleModal(e, sess.session_id)}
                    title={isKhmer ? 'លុបការសន្ទនានេះ' : 'Delete chat'}
                    className={`p-1 rounded-lg text-slate-400 dark:text-slate-500 hover:text-rose-600 dark:hover:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-all duration-300 cursor-pointer shrink-0 ${
                      isCollapsed ? 'max-w-0 p-0 opacity-0 pointer-events-none' : 'max-w-[30px] opacity-0 group-hover:opacity-100'
                    }`}
                  >
                    <Trash2 size={13} />
                  </button>
                </div>
              );
            })
          )}
        </div>

        {/* User Profile & Settings Section at Bottom */}
        <div className="p-3 border-t border-[#f3f4f6] dark:border-[#27272a] bg-white dark:bg-[#18181b]">
          <div className={`flex items-center transition-all duration-300 ease-in-out ${isCollapsed ? 'justify-center' : 'justify-between'}`}>
            <div className="flex items-center min-w-0">
              <button
                onClick={onOpenSettings}
                className="w-9 h-9 rounded-full bg-[#003E83] text-white flex items-center justify-center text-xs font-bold shrink-0 hover:opacity-90 transition-opacity cursor-pointer"
                title={isCollapsed ? (userProfile.name || (isKhmer ? 'គណនី & ការកំណត់' : 'Profile & Settings')) : ''}
              >
                {userProfile.name ? userProfile.name.charAt(0).toUpperCase() : <User size={16} />}
              </button>

              <div
                className={`min-w-0 overflow-hidden transition-all duration-300 ease-in-out ${
                  isCollapsed ? 'max-w-0 opacity-0 ml-0' : 'max-w-[150px] opacity-100 ml-2.5'
                }`}
              >
                <p className="text-xs font-semibold text-[#111827] dark:text-[#f4f4f5] truncate whitespace-nowrap">
                  {userProfile.name || (isKhmer ? 'ភ្ញៀវទេសចរ' : 'Traveler')}
                </p>
                <p className="text-[10px] text-[#6b7280] dark:text-[#a1a1aa] truncate whitespace-nowrap">
                  {isKhmer ? 'អ្នករៀបចំដំណើរកម្សាន្ត' : 'Cambodia Tourist'}
                </p>
              </div>
            </div>

            <button
              onClick={onOpenSettings}
              className={`p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#27272a] transition-all duration-300 cursor-pointer ${
                isCollapsed ? 'max-w-0 p-0 opacity-0 pointer-events-none' : 'max-w-[40px] opacity-100'
              }`}
              title="Settings"
            >
              <Settings size={16} />
            </button>
          </div>
        </div>

      </aside>

      {/* Delete Confirmation Modal */}
      {deleteModal.isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 dark:bg-slate-950/70 backdrop-blur-md animate-fade-in">
          <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-100 dark:border-slate-800 max-w-md w-full p-6 relative">
            <button
              onClick={() => setDeleteModal({ isOpen: false, deleteScope: 'ONE', selectedSessionId: '' })}
              className="absolute top-4 right-4 text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              <X size={18} />
            </button>

            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-rose-100 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0">
                <Trash2 size={20} />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  {isKhmer ? 'លុបការសន្ទនា' : 'Delete Chat History'}
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  {isKhmer ? 'សូមជ្រើសរើសជម្រើសលុបប្រវត្តិសន្ទនា' : 'Choose to delete 1 chat or clear all history.'}
                </p>
              </div>
            </div>

            <div className="space-y-3 mb-6">
              <label
                onClick={() => setDeleteModal(prev => ({ ...prev, deleteScope: 'ONE' }))}
                className={`flex items-start p-3 rounded-xl border cursor-pointer transition-all ${
                  deleteModal.deleteScope === 'ONE'
                    ? 'border-[#0F766E] dark:border-[#14B8A6] bg-teal-50/40 dark:bg-teal-950/30 text-slate-900 dark:text-white ring-1 ring-[#0F766E]'
                    : 'border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
                }`}
              >
                <input
                  type="radio"
                  name="deleteScope"
                  checked={deleteModal.deleteScope === 'ONE'}
                  onChange={() => setDeleteModal(prev => ({ ...prev, deleteScope: 'ONE' }))}
                  className="mt-0.5 text-[#0F766E]"
                />
                <div className="ml-3 flex-1">
                  <span className="block text-xs font-bold text-slate-900 dark:text-white">
                    {isKhmer ? 'លុប ១ ការសន្ទនា' : 'Delete Single Chat'}
                  </span>
                  {deleteModal.deleteScope === 'ONE' && (
                    <div className="mt-2">
                      <select
                        value={deleteModal.selectedSessionId || (sessions[0]?.session_id || '')}
                        onChange={(e) => setDeleteModal(prev => ({ ...prev, selectedSessionId: e.target.value }))}
                        className="w-full p-2 text-xs bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-800 dark:text-slate-200 font-medium focus:outline-none"
                      >
                        {sessions.map((s, i) => (
                          <option key={s.session_id || i} value={s.session_id}>
                            {s.title || `Chat Session #${i + 1}`}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>
              </label>

              <label
                onClick={() => setDeleteModal(prev => ({ ...prev, deleteScope: 'ALL' }))}
                className={`flex items-start p-3 rounded-xl border cursor-pointer transition-all ${
                  deleteModal.deleteScope === 'ALL'
                    ? 'border-rose-500 bg-rose-50/40 dark:bg-rose-950/30 text-slate-900 dark:text-white ring-1 ring-rose-500'
                    : 'border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'
                }`}
              >
                <input
                  type="radio"
                  name="deleteScope"
                  checked={deleteModal.deleteScope === 'ALL'}
                  onChange={() => setDeleteModal(prev => ({ ...prev, deleteScope: 'ALL' }))}
                  className="mt-0.5 text-rose-600"
                />
                <div className="ml-3">
                  <span className="block text-xs font-bold text-rose-700 dark:text-rose-400">
                    {isKhmer ? 'លុបការសន្ទនាទាំងអស់' : 'Delete All Chat History'}
                  </span>
                </div>
              </label>
            </div>

            <div className="flex items-center space-x-3 pt-2 border-t border-slate-100 dark:border-slate-800">
              <button
                onClick={() => setDeleteModal({ isOpen: false, deleteScope: 'ONE', selectedSessionId: '' })}
                className="flex-1 py-2 px-4 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 font-medium text-xs transition-colors"
              >
                {isKhmer ? 'បោះបង់' : 'Cancel'}
              </button>
              <button
                onClick={handleConfirmDelete}
                className="flex-1 py-2 px-4 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-medium text-xs shadow-sm transition-all"
              >
                {isKhmer ? 'លុប' : 'Confirm Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Sidebar;
