import React from 'react';
import { Compass, Globe, Menu, X, Sparkles, Wifi, WifiOff, AlertTriangle, Sun, Moon } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

const Header = ({
  language,
  setLanguage,
  isMobileMenuOpen,
  setIsMobileMenuOpen,
  isOnline,
  mode = 'online'
}) => {
  const { isDarkMode, toggleTheme } = useTheme();

  const toggleLanguage = (lang) => {
    setLanguage(lang);
  };

  return (
    <header className="bg-white dark:bg-[#1E293B] border-b border-[#E2E8F0] dark:border-slate-800 sticky top-0 z-30 shadow-xs transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Left Side: Brand Logo & Title */}
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 rounded-lg text-slate-600 dark:text-slate-300 hover:text-[#0F766E] dark:hover:text-[#14B8A6] hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            aria-label="Toggle sidebar"
          >
            {isMobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>

          <div className="flex items-center space-x-2.5">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#0F766E] to-[#14B8A6] flex items-center justify-center text-white shadow-md shadow-[#0F766E]/20">
              <Compass size={24} className="animate-spin-slow" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="font-bold text-lg text-[#0F172A] dark:text-white tracking-tight">
                  AIChat_Support
                </h1>
                <span className="inline-flex items-center gap-1 text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-[#14B8A6]/10 text-[#0F766E] dark:text-[#14B8A6] border border-[#14B8A6]/20">
                  <Sparkles size={10} /> Cambodia AI
                </span>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 hidden sm:block">
                {language === 'km' ? 'ជំនួយការទេសចរណ៍ឆ្លាតវៃកម្ពុជា' : 'Cambodia AI Tourism Assistant'}
              </p>
            </div>
          </div>
        </div>

        {/* Right Side: Connection Status Badge, Theme Toggle & Language Switcher */}
        <div className="flex items-center space-x-2 sm:space-x-3">
          
          {/* Status Indicator Badge */}
          {!isOnline ? (
            <div className="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs font-semibold">
              <WifiOff size={14} className="text-slate-500 dark:text-slate-400" />
              <span className="hidden sm:inline">Offline Mode</span>
            </div>
          ) : mode === 'fallback' ? (
            <div className="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 text-amber-800 dark:text-amber-300 text-xs font-semibold">
              <AlertTriangle size={14} className="text-amber-500" />
              <span className="hidden sm:inline">Local Fallback</span>
            </div>
          ) : (
            <div className="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60 text-emerald-700 dark:text-emerald-300 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <Wifi size={14} className="text-emerald-600 dark:text-emerald-400" />
              <span className="hidden sm:inline">Online AI</span>
            </div>
          )}

          {/* Dark / Light Mode Toggle Button */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-amber-400 hover:text-slate-900 dark:hover:text-amber-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer"
            aria-label={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
            title={isDarkMode ? (language === 'km' ? 'ប្តូរទៅ Dark Mode' : 'Switch to Light Mode') : (language === 'km' ? 'ប្តូរទៅ Light Mode' : 'Switch to Dark Mode')}
          >
            {isDarkMode ? <Sun size={18} className="text-amber-400" /> : <Moon size={18} className="text-slate-700" />}
          </button>

          {/* Language Switcher */}
          <div className="flex items-center bg-slate-100 dark:bg-slate-800 p-1 rounded-xl border border-slate-200 dark:border-slate-700">
            <button
              onClick={() => toggleLanguage('en')}
              className={`flex items-center space-x-1 px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                language === 'en'
                  ? 'bg-white dark:bg-slate-700 text-[#0F766E] dark:text-[#14B8A6] shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              <span>🇬🇧</span>
              <span>EN</span>
            </button>
            <button
              onClick={() => toggleLanguage('km')}
              className={`flex items-center space-x-1 px-2.5 sm:px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                language === 'km'
                  ? 'bg-white dark:bg-slate-700 text-[#0F766E] dark:text-[#14B8A6] shadow-xs'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
              }`}
            >
              <span>🇰🇭</span>
              <span>KM</span>
            </button>
          </div>
        </div>

      </div>
    </header>
  );
};

export default Header;

