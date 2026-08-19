import React from 'react';
import { Sparkles } from 'lucide-react';

const TypingIndicator = ({ language = 'en' }) => {
  const isKhmer = language === 'km';

  return (
    <div className="flex items-start space-x-3 mb-6 animate-fade-in">
      {/* Bot Avatar */}
      <div className="w-9 h-9 rounded-2xl bg-[#2563eb] text-white flex items-center justify-center shrink-0 shadow-sm">
        <Sparkles size={18} className="animate-spin-slow" />
      </div>

      {/* Typing Bubble */}
      <div className="bg-white dark:bg-[#18181b] border border-slate-200/90 dark:border-[#27272a] px-4 py-3 rounded-2xl rounded-tl-xs shadow-2xs flex items-center space-x-2.5">
        <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">
          {isKhmer ? 'Angkor Verse AI កំពុងគិត...' : 'Angkor Verse AI is thinking'}
        </span>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 rounded-full bg-[#2563eb] typing-dot"></div>
          <div className="w-2 h-2 rounded-full bg-[#003E83] typing-dot"></div>
          <div className="w-2 h-2 rounded-full bg-slate-900 dark:bg-white typing-dot"></div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
