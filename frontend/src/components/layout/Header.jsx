import React from 'react';
import { Sparkles, WifiOff, AlertTriangle, Settings, Plus } from 'lucide-react';

const Header = ({
  language,
  isOnline,
  mode = 'online',
  onOpenSettings,
  onNewChat
}) => {
  const isKhmer = language === 'km';

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
            <div>
              <span className="font-extrabold text-sm sm:text-base tracking-tight text-slate-900 dark:text-white truncate block">
                Angkor Verse AI
              </span>
              <span className="hidden sm:block text-[10px] text-slate-400 dark:text-slate-500 -mt-0.5">
                Cambodia Tourism Intelligence
              </span>
            </div>
          </div>

          {/* Model Selector Badge (Desktop) */}
          <div className="hidden lg:flex items-center space-x-1.5 h-7 px-2.5 rounded-full bg-slate-100 dark:bg-[#27272a] border border-slate-200 dark:border-[#27272a] text-slate-700 dark:text-slate-300 text-[11px] font-semibold">
            <Sparkles size={12} className="text-[#003E83] dark:text-blue-400" />
            <span>Angkor Verse 2.5</span>
          </div>
        </div>

        {/* Right Side: New Chat, Status Badge & Settings */}
        <div className="flex items-center space-x-2 shrink-0">

          {/* New Chat Button */}
          <button
            onClick={onNewChat}
            className="flex items-center space-x-1.5 h-8 px-3.5 rounded-full bg-[#003E83] hover:bg-[#002e62] dark:bg-[#2563eb] dark:hover:bg-[#1d4ed8] text-white text-xs font-bold shadow-xs transition-all duration-200 active:scale-95 cursor-pointer shrink-0"
            title={isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat'}
          >
            <Plus size={14} className="shrink-0" />
            <span className="text-xs">
              {isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat'}
            </span>
          </button>

          {/* Status Indicator Badge */}
          <div className="hidden sm:flex items-center">
            {!isOnline || mode === 'offline' ? (
              <div
                className="flex items-center space-x-1.5 h-8 px-3 rounded-full bg-slate-100 dark:bg-slate-800/80 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs font-semibold"
                title="Running on local offline model & database"
              >
                <WifiOff size={13} className="text-slate-500" />
                <span>Offline</span>
              </div>
            ) : mode === 'degraded' || mode === 'fallback' ? (
              <div
                className="flex items-center space-x-1.5 h-8 px-3 rounded-full bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 text-amber-800 dark:text-amber-300 text-xs font-semibold"
                title="Cached data mode active"
              >
                <AlertTriangle size={13} className="text-amber-500" />
                <span>Offline</span>
              </div>
            ) : (
              <div
                className="flex items-center space-x-1.5 h-8 px-3 rounded-full bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 text-emerald-700 dark:text-emerald-300 text-xs font-semibold"
                title="Connected to Online AI & Real-Time Services"
              >
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
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
            <Settings size={15} />
          </button>
        </div>

      </div>
    </header>
  );
};

export default Header;
