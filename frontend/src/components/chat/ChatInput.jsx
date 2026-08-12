import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, MapPin, Hotel, Utensils, Calendar } from 'lucide-react';

const ChatInput = ({ onSendMessage, isLoading, language = 'en' }) => {
  const [text, setText] = useState('');
  const textareaRef = useRef(null);
  const isKhmer = language === 'km';

  // Auto-resize textarea based on input content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [text]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim() || isLoading) return;
    onSendMessage(text.trim());
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="bg-white dark:bg-[#1E293B] border-t border-[#E2E8F0] dark:border-slate-800 p-3 sm:p-4 sticky bottom-0 z-20 transition-colors duration-200">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="relative flex items-end bg-slate-50 dark:bg-slate-900/80 border border-[#E2E8F0] dark:border-slate-700 focus-within:border-[#0F766E] dark:focus-within:border-[#14B8A6] focus-within:ring-2 focus-within:ring-[#0F766E]/20 dark:focus-within:ring-[#14B8A6]/20 rounded-2xl p-2 transition-all shadow-xs">
          
          {/* Text Area Input */}
          <textarea
            ref={textareaRef}
            rows={1}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              isKhmer
                ? 'សួរអំពីតំបន់ទេសចរណ៍ សណ្ឋាគារ ហាងអាហារនៅកម្ពុជា...'
                : 'Ask about Cambodia places, hotels, food, ticket fees...'
            }
            disabled={isLoading}
            className="w-full bg-transparent text-sm text-[#0F172A] dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none resize-none px-3 py-2 max-h-32 min-h-[42px]"
          />

          {/* Send Button */}
          <button
            type="submit"
            disabled={!text.trim() || isLoading}
            className={`p-2.5 rounded-xl text-white font-medium flex items-center justify-center shrink-0 transition-all ${
              text.trim() && !isLoading
                ? 'bg-gradient-to-r from-[#0F766E] to-[#14B8A6] hover:opacity-95 shadow-md shadow-[#0F766E]/20 active:scale-95 cursor-pointer'
                : 'bg-slate-300 dark:bg-slate-800 text-slate-400 dark:text-slate-600 cursor-not-allowed'
            }`}
            aria-label="Send message"
          >
            <Send size={18} />
          </button>
        </div>

        <p className="text-[11px] text-center text-slate-400 dark:text-slate-500 mt-2">
          {isKhmer
            ? 'AIChat_Support ផ្តល់ព័ត៌មានទេសចរណ៍ផ្លូវការចេញពីទិន្នន័យទេសចរណ៍កម្ពុជា'
            : 'AIChat_Support provides verified Cambodian tourism insights grounded in database context.'}
        </p>
      </form>
    </div>
  );
};

export default ChatInput;
