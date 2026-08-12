import React from 'react';
import { Compass, Globe, Menu, X, Sparkles, Wifi, WifiOff, AlertTriangle, Sun, Moon, Settings, ChevronDown } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

const Header = ({
  language,
  setLanguage,
  isMobileMenuOpen,
  setIsMobileMenuOpen,
  isOnline,
  mode = 'online',
  onOpenSettings,
  isSidebarCollapsed,
  onToggleSidebarCollapse
}) => {
  const { isDarkMode, toggleTheme } = useTheme();

  const toggleLanguage = (lang) => {
    setLanguage(lang);
  };

  return (
    <header className="bg-white/80 dark:bg-[#18181b]/80 backdrop-blur-md border-b border-[#f3f4f6] dark:border-[#27272a] sticky top-0 z-30 transition-colors duration-200">
      <div className="w-full px-4 sm:px-6 h-14 flex items-center justify-between">
        
        {/* Left Side: Mobile Hamburger, Desktop Collapse Toggle & Brand Logo */}
        <div className="flex items-center space-x-3">
          {/* Mobile Drawer Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:text-[#003E83] dark:hover:text-[#2563eb] hover:bg-slate-100 dark:hover:bg-[#27272a] transition-colors"
            aria-label="Toggle mobile menu"
          >
            {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>

          {/* Desktop Sidebar Collapse Toggle Button */}
          <button
            onClick={onToggleSidebarCollapse}
            className="hidden md:flex p-2 rounded-xl text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#27272a] transition-colors cursor-pointer"
            aria-label="Toggle sidebar collapse"
            title={isSidebarCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            <Menu size={19} />
          </button>

          {/* Brand Logo & Model Pill */}
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-[#003E83] flex items-center justify-center text-white shadow-sm">
              <Compass size={22} className="animate-spin-slow" />
            </div>
            
            <div className="flex items-center space-x-2">
              <span className="font-bold text-base tracking-tight text-slate-900 dark:text-white hidden sm:inline">
                Cambodia AI
              </span>

              {/* Model Selector Badge */}
              <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-100 dark:bg-[#27272a] border border-[#f3f4f6] dark:border-[#27272a] text-slate-700 dark:text-slate-300 text-xs font-semibold hover:bg-slate-200 dark:hover:bg-[#3f3f46] transition-colors cursor-pointer">
                <Sparkles size={13} className="text-[#2563eb]" />
                <span className="text-[11px]">Tourism AI v2.5</span>
                <ChevronDown size={12} className="text-slate-400" />
              </div>
            </div>
          </div>
        </div>

        {/* Right Side: Status Badge, Dark Mode, Language & Settings */}
        <div className="flex items-center space-x-2">
          
          {/* Status Indicator Badge */}
          {!isOnline ? (
            <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs font-medium">
              <WifiOff size={13} className="text-slate-500" />
              <span className="hidden sm:inline text-[11px]">Offline</span>
            </div>
          ) : mode === 'fallback' ? (
            <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 text-amber-800 dark:text-amber-300 text-xs font-medium">
              <AlertTriangle size={13} className="text-amber-500" />
              <span className="hidden sm:inline text-[11px]">Fallback</span>
            </div>
          ) : (
            <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800/60 text-blue-700 dark:text-blue-300 text-xs font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></span>
              <Wifi size={13} className="text-blue-600 dark:text-blue-400" />
              <span className="hidden sm:inline text-[11px]">Online</span>
            </div>
          )}

          {/* Dark / Light Mode Toggle Button */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-amber-400 hover:text-slate-900 dark:hover:text-amber-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer"
            aria-label="Toggle dark mode"
            title={isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
          >
            {isDarkMode ? <Sun size={17} className="text-amber-400" /> : <Moon size={17} className="text-slate-700" />}
          </button>

          {/* Language Switcher */}
          <div className="flex items-center bg-slate-100 dark:bg-slate-800/80 p-1 rounded-xl border border-slate-200 dark:border-slate-700">
            <button
              onClick={() => toggleLanguage('en')}
              className={`px-2 py-1 rounded-lg text-xs font-semibold transition-all ${
                language === 'en'
                  ? 'bg-white dark:bg-slate-700 text-[#0F766E] dark:text-[#14B8A6] shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              EN
            </button>
            <button
              onClick={() => toggleLanguage('km')}
              className={`px-2 py-1 rounded-lg text-xs font-semibold transition-all ${
                language === 'km'
                  ? 'bg-white dark:bg-slate-700 text-[#0F766E] dark:text-[#14B8A6] shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              KM
            </button>
          </div>

          {/* Settings Modal Launcher Button */}
          <button
            onClick={onOpenSettings}
            className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer"
            title="Settings & Profile"
          >
            <Settings size={17} />
          </button>
        </div>

      </div>
    </header>
  );
};

export default Header;


