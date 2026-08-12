import React from 'react';
import { Bot } from 'lucide-react';

const TypingIndicator = ({ language = 'en' }) => {
  const isKhmer = language === 'km';

  return (
    <div className="flex items-start space-x-3 mb-4 animate-fade-in">
      {/* Bot Avatar */}
      <div className="w-8 h-8 rounded-full bg-[#0F766E] text-white flex items-center justify-center shrink-0 shadow-sm">
        <Bot size={18} />
      </div>

      {/* Typing Bubble */}
      <div className="bg-white dark:bg-slate-800 border border-[#E2E8F0] dark:border-slate-700 px-4 py-3 rounded-2xl rounded-tl-sm shadow-sm flex items-center space-x-2">
        <span className="text-xs text-slate-500 dark:text-slate-400 font-medium mr-1">
          {isKhmer ? 'កំពុងគិត...' : 'AI is thinking'}
        </span>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 rounded-full bg-[#14B8A6] typing-dot"></div>
          <div className="w-2 h-2 rounded-full bg-[#0F766E] typing-dot"></div>
          <div className="w-2 h-2 rounded-full bg-[#0F172A] dark:bg-white typing-dot"></div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
