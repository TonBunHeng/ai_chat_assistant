import React, { useState, useEffect } from 'react';
import { X, Settings, Moon, Sun, Globe, User, MapPin, Sliders, ShieldCheck, Check, Sparkles, Search, ChevronDown, Bell, Lock, Palette, Info } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

const SettingsModal = ({ isOpen, onClose, language, setLanguage, userProfile, setUserProfile }) => {
  const { isDarkMode, toggleTheme } = useTheme();
  const [activeTab, setActiveTab] = useState('general');
  const [searchQuery, setSearchQuery] = useState('');
  const [shouldRender, setShouldRender] = useState(isOpen);
  const [animateIn, setAnimateIn] = useState(false);
  const isKhmer = language === 'km';

  // Smooth open and close animation state management
  useEffect(() => {
    let frameId;
    if (isOpen) {
      setShouldRender(true);
      frameId = requestAnimationFrame(() => {
        requestAnimationFrame(() => setAnimateIn(true));
      });
    } else {
      setAnimateIn(false);
      const timer = setTimeout(() => setShouldRender(false), 250);
      return () => clearTimeout(timer);
    }
    return () => {
      if (frameId) cancelAnimationFrame(frameId);
    };
  }, [isOpen]);

  // Handle ESC key to close smoothly
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!shouldRender) return null;

  const destinations = [
    { id: 'siem_reap', nameEn: 'Siem Reap (Angkor)', nameKm: 'សៀមរាប (អង្គរ)' },
    { id: 'phnom_penh', nameEn: 'Phnom Penh', nameKm: 'ភ្នំពេញ' },
    { id: 'kampot', nameEn: 'Kampot & Kep', nameKm: 'កំពត និង កែប' },
    { id: 'islands', nameEn: 'Koh Rong & Islands', nameKm: 'កោះរ៉ុង និង កោះកែប' },
  ];

  const travelStyles = [
    { id: 'cultural', nameEn: 'Cultural & Heritage', nameKm: 'វប្បធម៌ និង បេតិកភណ្ឌ' },
    { id: 'foodie', nameEn: 'Food & Culinary', nameKm: 'ម្ហូបអាហារ និង ភេសជ្ជៈ' },
    { id: 'adventure', nameEn: 'Nature & Adventure', nameKm: 'ធម្មជាតិ និង ផ្សងព្រេង' },
    { id: 'luxury', nameEn: 'Relaxation & Resorts', nameKm: 'លំហែកាយ និង សម្រាក' },
  ];

  const toggleDestination = (id) => {
    setUserProfile((prev) => {
      const current = prev.preferredDestinations || [];
      const updated = current.includes(id)
        ? current.filter((item) => item !== id)
        : [...current, id];
      return { ...prev, preferredDestinations: updated };
    });
  };

  const setTravelStyle = (styleId) => {
    setUserProfile((prev) => ({ ...prev, travelStyle: styleId }));
  };

  const tabs = [
    { id: 'general', labelEn: 'General', labelKm: 'ទូទៅ', icon: <Settings size={17} /> },
    { id: 'profile', labelEn: 'Account', labelKm: 'គណនី', icon: <User size={17} /> },
    { id: 'travel', labelEn: 'Personalization', labelKm: 'ចំណូលចិត្តផ្ទាល់ខ្លួន', icon: <Sparkles size={17} /> },
    { id: 'about', labelEn: 'About', labelKm: 'អំពីប្រព័ន្ធ', icon: <Info size={17} /> },
  ];

  const filteredTabs = tabs.filter(t => 
    t.labelEn.toLowerCase().includes(searchQuery.toLowerCase()) || 
    t.labelKm.includes(searchQuery)
  );

  return (
    <div
      onClick={onClose}
      className={`fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 transition-all duration-200 ease-out ${
        animateIn
          ? 'bg-black/60 backdrop-blur-xs opacity-100'
          : 'bg-black/0 backdrop-blur-none opacity-0 pointer-events-none'
      }`}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className={`bg-[#ffffff] dark:bg-[#18181b] rounded-2xl shadow-2xl border border-slate-200/80 dark:border-[#27272a] w-full max-w-[680px] h-[520px] max-h-[88vh] flex flex-col sm:flex-row overflow-hidden transform transition-all duration-200 ease-out ${
          animateIn
            ? 'opacity-100 scale-100 translate-y-0'
            : 'opacity-0 scale-95 translate-y-2'
        }`}
      >
        
        {/* Left Sidebar (ChatGPT-Style) */}
        <div className="sm:w-[210px] bg-slate-50/60 dark:bg-[#141416] p-3 sm:p-3.5 border-b sm:border-b-0 sm:border-r border-slate-100 dark:border-[#27272a] flex flex-col shrink-0">
          
          {/* Top Left Close Button & Header */}
          <div className="flex items-center justify-between mb-3">
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-200/70 dark:hover:bg-[#27272a] transition-colors cursor-pointer"
              title="Close"
            >
              <X size={18} />
            </button>
            <span className="sm:hidden font-semibold text-xs text-slate-800 dark:text-slate-200">
              {isKhmer ? 'ការកំណត់' : 'Settings'}
            </span>
          </div>

          {/* Search Input Box */}
          <div className="relative mb-2.5">
            <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={isKhmer ? 'ស្វែងរក...' : 'Search settings'}
              className="w-full pl-8 pr-2.5 py-1.5 bg-white dark:bg-[#1f1f23] border border-slate-200 dark:border-[#27272a] rounded-lg text-xs text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-slate-400 dark:focus:ring-slate-600 transition-all"
            />
          </div>

          {/* Tab Navigation List */}
          <div className="flex sm:flex-col overflow-x-auto sm:overflow-x-visible gap-1 flex-1 scrollbar-none">
            {(filteredTabs.length > 0 ? filteredTabs : tabs).map((tab) => {
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2.5 px-3 py-2 rounded-lg text-xs font-medium transition-all text-left cursor-pointer shrink-0 sm:w-full ${
                    isActive
                      ? 'bg-slate-200/80 dark:bg-[#27272a] text-slate-900 dark:text-white font-semibold'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#1f1f23]'
                  }`}
                >
                  <span className={isActive ? 'text-slate-900 dark:text-white' : 'text-slate-400 dark:text-slate-500'}>
                    {tab.icon}
                  </span>
                  <span className="truncate">{isKhmer ? tab.labelKm : tab.labelEn}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Content Area (ChatGPT Row-by-Row Style) */}
        <div className="flex-1 overflow-y-auto px-5 sm:px-6 py-4 sm:py-5 flex flex-col bg-white dark:bg-[#18181b]">
          
          {/* Active Tab Title Header */}
          <div className="pb-3 mb-1 border-b border-slate-100 dark:border-[#27272a]">
            <h2 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white">
              {activeTab === 'general' && (isKhmer ? 'ទូទៅ (General)' : 'General')}
              {activeTab === 'profile' && (isKhmer ? 'គណនី (Account)' : 'Account')}
              {activeTab === 'travel' && (isKhmer ? 'ចំណូលចិត្តផ្ទាល់ខ្លួន (Personalization)' : 'Personalization')}
              {activeTab === 'about' && (isKhmer ? 'អំពីប្រព័ន្ធ (About)' : 'About')}
            </h2>
          </div>

          {/* Tab 1: General */}
          {activeTab === 'general' && (
            <div className="flex-1 divide-y divide-slate-100 dark:divide-[#27272a]">
              
              {/* Row 1: Appearance / Theme */}
              <div className="py-3.5 flex items-center justify-between">
                <div>
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    {isKhmer ? 'ស្បែកចំណុចប្រទាក់' : 'Appearance'}
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    {isKhmer ? 'ជ្រើសរើសស្បែកពណ៌' : 'Choose color theme'}
                  </div>
                </div>

                <div className="flex items-center bg-slate-100 dark:bg-[#27272a] p-0.5 rounded-lg border border-slate-200 dark:border-[#333338]">
                  <button
                    onClick={() => { if (isDarkMode) toggleTheme(); }}
                    className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs transition-all cursor-pointer ${
                      !isDarkMode
                        ? 'bg-white dark:bg-[#18181b] text-slate-900 dark:text-white font-semibold shadow-2xs'
                        : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    <Sun size={13} className="text-amber-500" />
                    <span>Light</span>
                  </button>
                  <button
                    onClick={() => { if (!isDarkMode) toggleTheme(); }}
                    className={`flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs transition-all cursor-pointer ${
                      isDarkMode
                        ? 'bg-white dark:bg-[#18181b] text-slate-900 dark:text-white font-semibold shadow-2xs'
                        : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                    }`}
                  >
                    <Moon size={13} className="text-indigo-400" />
                    <span>Dark</span>
                  </button>
                </div>
              </div>

              {/* Row 2: Language */}
              <div className="py-3.5 flex items-center justify-between">
                <div>
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    {isKhmer ? 'ភាសា' : 'Language'}
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    {isKhmer ? 'ភាសាឆ្លើយតបចម្បង' : 'Primary conversation language'}
                  </div>
                </div>

                <div className="relative">
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="appearance-none bg-slate-100 dark:bg-[#27272a] border border-slate-200 dark:border-[#333338] text-slate-900 dark:text-white text-xs font-medium rounded-lg px-3 py-1.5 pr-7 focus:outline-none cursor-pointer"
                  >
                    <option value="en">English (US)</option>
                    <option value="km">ភាសាខ្មែរ (Khmer)</option>
                  </select>
                  <ChevronDown size={13} className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
                </div>
              </div>

              {/* Row 3: Offline Data Cache */}
              <div className="py-3.5 flex items-center justify-between">
                <div>
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    {isKhmer ? 'ទិន្នន័យក្រៅបណ្តាញ' : 'Offline RAG Knowledge'}
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    {isKhmer ? 'ស្វែងរកទិន្នន័យទេសចរណ៍ទោះគ្មានអ៊ីនធឺណិត' : 'Search local tourism data even without network'}
                  </div>
                </div>

                <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800 text-[11px] font-medium">
                  Active
                </span>
              </div>

              {/* Row 4: Verified Tourism Data */}
              <div className="py-3.5 flex items-center justify-between">
                <div>
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    {isKhmer ? 'ប្រភពទិន្នន័យ' : 'Knowledge Source'}
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    {isKhmer ? 'ផ្អែកលើទិន្នន័យទេសចរណ៍ផ្លូវការកម្ពុជា' : 'Cambodia Tourism Official Database'}
                  </div>
                </div>

                <ShieldCheck size={18} className="text-blue-500" />
              </div>
            </div>
          )}

          {/* Tab 2: Profile */}
          {activeTab === 'profile' && (
            <div className="flex-1 divide-y divide-slate-100 dark:divide-[#27272a]">
              {/* Row 1: Display Name */}
              <div className="py-3.5 flex items-center justify-between gap-4">
                <div className="shrink-0">
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    {isKhmer ? 'ឈ្មោះអ្នកប្រើប្រាស់' : 'Display Name'}
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    {isKhmer ? 'ឈ្មោះដែល AI ប្រើសម្រាប់ហៅអ្នក' : 'Name used in AI greetings'}
                  </div>
                </div>

                <input
                  type="text"
                  value={userProfile.name || ''}
                  onChange={(e) => setUserProfile({ ...userProfile, name: e.target.value })}
                  placeholder="Traveler"
                  className="w-44 sm:w-56 px-3 py-1.5 text-xs bg-slate-100 dark:bg-[#27272a] border border-slate-200 dark:border-[#333338] rounded-lg text-slate-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-slate-400"
                />
              </div>

              {/* Row 2: Email */}
              <div className="py-3.5 flex items-center justify-between gap-4">
                <div className="shrink-0">
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    {isKhmer ? 'អ៊ីមែល (មិនបាច់បំពេញ)' : 'Email'}
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    {isKhmer ? 'សម្រាប់ទទួលព័ត៌មានធ្វើដំណើរ' : 'Optional contact'}
                  </div>
                </div>

                <input
                  type="email"
                  value={userProfile.email || ''}
                  onChange={(e) => setUserProfile({ ...userProfile, email: e.target.value })}
                  placeholder="user@example.com"
                  className="w-44 sm:w-56 px-3 py-1.5 text-xs bg-slate-100 dark:bg-[#27272a] border border-slate-200 dark:border-[#333338] rounded-lg text-slate-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-slate-400"
                />
              </div>

              {/* Row 3: Local Storage Note */}
              <div className="py-3.5 flex items-center justify-between">
                <div>
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    {isKhmer ? 'ការរក្សាទុកទិន្នន័យ' : 'Data Privacy'}
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    {isKhmer ? 'រក្សាទុកក្នុងឧបករណ៍របស់អ្នកដោយសុវត្ថិភាព' : 'Stored securely in local browser storage'}
                  </div>
                </div>

                <Lock size={16} className="text-slate-400" />
              </div>
            </div>
          )}

          {/* Tab 3: Personalization / Travel Style */}
          {activeTab === 'travel' && (
            <div className="flex-1 divide-y divide-slate-100 dark:divide-[#27272a]">
              
              {/* Row 1: Travel Persona */}
              <div className="py-3.5 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                      {isKhmer ? 'ស្ទីលនៃការដើរលេង' : 'Travel Style'}
                    </div>
                    <div className="text-[11px] text-slate-400 dark:text-slate-500">
                      {isKhmer ? 'ជ្រើសរើសស្ទីលដើម្បីឱ្យ AI ណែនាំត្រូវចំណូលចិត្ត' : 'Helps AI suggest tailored attractions & tips'}
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2 mt-1">
                  {travelStyles.map((style) => {
                    const isSelected = userProfile.travelStyle === style.id;
                    return (
                      <button
                        key={style.id}
                        onClick={() => setTravelStyle(style.id)}
                        className={`px-3 py-2 rounded-lg text-xs text-left transition-all border cursor-pointer ${
                          isSelected
                            ? 'bg-slate-100 dark:bg-[#27272a] border-slate-400 dark:border-slate-500 font-semibold text-slate-900 dark:text-white'
                            : 'border-slate-200 dark:border-[#27272a] text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#1f1f23]'
                        }`}
                      >
                        {isKhmer ? style.nameKm : style.nameEn}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Row 2: Favorite Destinations */}
              <div className="py-3.5 flex flex-col gap-2">
                <div>
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    {isKhmer ? 'ខេត្ត/ក្រុងដែលចូលចិត្ត' : 'Favorite Destinations'}
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    {isKhmer ? 'ជ្រើសរើសខេត្ត/ក្រុងដែលចង់ទៅកម្សាន្ត' : 'Select top Cambodian destinations'}
                  </div>
                </div>

                <div className="flex flex-wrap gap-1.5 mt-1">
                  {destinations.map((dest) => {
                    const isSelected = (userProfile.preferredDestinations || []).includes(dest.id);
                    return (
                      <button
                        key={dest.id}
                        onClick={() => toggleDestination(dest.id)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all border cursor-pointer flex items-center space-x-1.5 ${
                          isSelected
                            ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 border-transparent shadow-2xs font-semibold'
                            : 'bg-slate-100 dark:bg-[#27272a] text-slate-700 dark:text-slate-300 border-slate-200 dark:border-[#333338] hover:bg-slate-200/70'
                        }`}
                      >
                        <span>{isKhmer ? dest.nameKm : dest.nameEn}</span>
                        {isSelected && <Check size={12} />}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* Tab 4: About */}
          {activeTab === 'about' && (
            <div className="flex-1 divide-y divide-slate-100 dark:divide-[#27272a]">
              {/* Row 1: App Info */}
              <div className="py-3.5 flex items-center justify-between">
                <div>
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    Application
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    AI Tourism Information Service (Cambodia)
                  </div>
                </div>
                <div className="font-semibold text-xs text-slate-900 dark:text-white">
                  Angkor Verse AI
                </div>
              </div>

              {/* Row 2: Version */}
              <div className="py-3.5 flex items-center justify-between">
                <div>
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    Version
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    Current system release
                  </div>
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                  v2.5.0
                </div>
              </div>

              {/* Row 3: Focus */}
              <div className="py-3.5 flex items-center justify-between">
                <div>
                  <div className="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    Specialization
                  </div>
                  <div className="text-[11px] text-slate-400 dark:text-slate-500">
                    World Heritage, Temples, Culture & Travel Plans
                  </div>
                </div>
                <span className="text-xs font-medium text-slate-700 dark:text-slate-300">
                  Cambodia
                </span>
              </div>
            </div>
          )}

        </div>

      </div>
    </div>
  );
};

export default SettingsModal;
