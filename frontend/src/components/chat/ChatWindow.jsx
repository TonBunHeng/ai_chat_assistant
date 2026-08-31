import React, { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import TypingIndicator from './TypingIndicator';
import { AlertCircle } from 'lucide-react';

const ChatWindow = ({
  messages = [],
  isLoading = false,
  error = null,
  onSendMessage,
  onRegenerate,
  language = 'en'
}) => {
  const messagesEndRef = useRef(null);
  const isKhmer = language === 'km';

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto px-3 py-4 sm:px-6 sm:py-8 bg-[#f8fafc] dark:bg-[#18181b] transition-colors duration-200">
      <div className="max-w-4xl mx-auto space-y-4">
        
        {/* Active Chat Conversation Messages */}
        {messages.map((msg, index) => (
          <ChatMessage
            key={msg.id || index}
            message={msg}
            language={language}
            onRegenerate={onRegenerate}
            onSelectSuggestion={onSendMessage}
          />
        ))}

        {/* Loading / Typing Indicator */}
        {isLoading && <TypingIndicator language={language} />}

        {/* Error Alert Box */}
        {error && (
          <div className="my-4 p-4 rounded-2xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800/80 text-rose-800 dark:text-rose-300 text-sm flex items-start space-x-3 shadow-xs">
            <AlertCircle size={20} className="text-rose-500 shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="font-semibold">{isKhmer ? 'មានបញ្ហាក្នុងការតភ្ជាប់' : 'Connection Warning'}</p>
              <p className="text-xs text-rose-600 dark:text-rose-400 mt-0.5">{error}</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default ChatWindow;
