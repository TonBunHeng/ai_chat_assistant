import React from 'react';
import { Sparkles, WifiOff, AlertTriangle, Settings, ChevronDown, Plus } from 'lucide-react';

const Header = ({
  language,
  isOnline,
  mode = 'online',
  onOpenSettings,
  onNewChat
}) => {
  return (
    <header className="bg-white/95 dark:bg-[#18181b]/95 backdrop-blur-md border-b border-slate-100 dark:border-[#27272a] sticky top-0 z-30 transition-colors duration-200">
      <div className="w-full px-3 sm:px-6 h-14 flex items-center justify-between gap-2">

        {/* Left Side: Brand Logo & Title */}
        <div className="flex items-center space-x-2.5 shrink-0 min-w-0">
          <div className="flex items-center space-x-2 shrink-0">
            <img
              src="/tourism_logo.png"
              alt="Angkor Verse AI Logo"
              className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl object-contain shadow-xs shrink-0"
            />
            <span className="font-bold text-sm sm:text-base tracking-tight text-slate-900 dark:text-white truncate">
              Angkor Verse AI
            </span>
          </div>

          {/* Model Selector Badge (Desktop) */}
          <div className="hidden md:flex items-center space-x-1.5 h-8 px-3 rounded-full bg-slate-100 dark:bg-[#27272a] border border-slate-200 dark:border-[#27272a] text-slate-700 dark:text-slate-300 text-xs font-semibold hover:bg-slate-200 dark:hover:bg-[#3f3f46] transition-colors cursor-pointer">
            <Sparkles size={13} className="text-[#2563eb]" />
            <span className="text-[11px]">AI v2.5</span>
            <ChevronDown size={12} className="text-slate-400" />
          </div>
        </div>

        {/* Right Side: New Chat, Status Badge & Settings */}
        <div className="flex items-center space-x-2 shrink-0">

          {/* New Chat Button */}
          <button
            onClick={onNewChat}
            className="flex items-center space-x-1.5 h-8 px-3.5 rounded-full bg-[#003E83] hover:bg-[#002e62] dark:bg-[#2563eb] dark:hover:bg-[#1d4ed8] text-white text-xs font-semibold shadow-xs transition-all duration-200 active:scale-95 cursor-pointer shrink-0"
            title={language === 'km' ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat'}
          >
            <Plus size={15} className="shrink-0" />
            <span className="text-xs">
              {language === 'km' ? 'ថ្មី' : 'New Chat'}
            </span>
          </button>

          {/* Status Indicator Badge (Near Settings) */}
          <div className="hidden sm:flex items-center">
            {!isOnline ? (
              <div className="flex items-center space-x-1.5 h-8 px-3 rounded-full bg-slate-100 dark:bg-slate-800/80 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs font-medium">
                <WifiOff size={13} className="text-slate-500" />
                <span>Offline</span>
              </div>
            ) : mode === 'fallback' ? (
              <div className="flex items-center space-x-1.5 h-8 px-3 rounded-full bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 text-amber-800 dark:text-amber-300 text-xs font-medium">
                <AlertTriangle size={13} className="text-amber-500" />
                <span>Fallback</span>
              </div>
            ) : (
              <div className="flex items-center space-x-1.5 h-8 px-3 rounded-full bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800/60 text-blue-700 dark:text-blue-300 text-xs font-medium">
                <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
                <span>Online</span>
              </div>
            )}
          </div>

          {/* Settings Modal Launcher Button */}
          <button
            onClick={onOpenSettings}
            className="w-8 h-8 rounded-full flex items-center justify-center bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer shrink-0"
            title="Settings & Profile"
          >
            <Settings size={16} />
          </button>
        </div>

      </div>
    </header>
  );
};

export default Header;


