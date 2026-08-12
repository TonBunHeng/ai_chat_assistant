import React, { useState } from 'react';
import { X, Settings, Moon, Sun, Globe, User, MapPin, Sliders, ShieldCheck, Check } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';

const SettingsModal = ({ isOpen, onClose, language, setLanguage, userProfile, setUserProfile }) => {
  const { isDarkMode, toggleTheme } = useTheme();
  const [activeTab, setActiveTab] = useState('general');
  const isKhmer = language === 'km';

  if (!isOpen) return null;

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

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fade-in">
      <div className="bg-white dark:bg-[#18181b] rounded-2xl shadow-2xl border border-[#f3f4f6] dark:border-[#27272a] max-w-xl w-full flex flex-col max-h-[85vh] overflow-hidden transform transition-all animate-in fade-in zoom-in-95 duration-200">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between p-5 border-b border-[#f3f4f6] dark:border-[#27272a]">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-[#003E83]/10 dark:bg-[#2563eb]/20 text-[#003E83] dark:text-[#60a5fa] flex items-center justify-center">
              <Settings size={22} />
            </div>
            <div>
              <h3 className="font-bold text-lg text-[#111827] dark:text-[#f4f4f5]">
                {isKhmer ? 'ការកំណត់ & គណនី' : 'Settings & Preferences'}
              </h3>
              <p className="text-xs text-[#6b7280] dark:text-[#a1a1aa]">
                {isKhmer ? 'កែសម្រួលបទពិសោធន៍ AI ទេសចរណ៍កម្ពុជា' : 'Customize your Cambodia Tourism AI experience'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 dark:text-slate-500 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#27272a] transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Modal Content Body */}
        <div className="flex flex-1 overflow-hidden">
          
          {/* Tabs Sidebar */}
          <div className="w-44 bg-slate-50/70 dark:bg-[#18181b] p-3 border-r border-[#f3f4f6] dark:border-[#27272a] space-y-1">
            <button
              onClick={() => setActiveTab('general')}
              className={`w-full flex items-center space-x-2.5 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'general'
                  ? 'bg-white dark:bg-[#27272a] text-[#003E83] dark:text-[#60a5fa] shadow-xs font-semibold'
                  : 'text-[#6b7280] dark:text-[#a1a1aa] hover:bg-slate-100 dark:hover:bg-[#27272a]/50'
              }`}
            >
              <Sliders size={16} />
              <span>{isKhmer ? 'ទូទៅ' : 'General'}</span>
            </button>
            
            <button
              onClick={() => setActiveTab('profile')}
              className={`w-full flex items-center space-x-2.5 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'profile'
                  ? 'bg-white dark:bg-[#27272a] text-[#003E83] dark:text-[#60a5fa] shadow-xs font-semibold'
                  : 'text-[#6b7280] dark:text-[#a1a1aa] hover:bg-slate-100 dark:hover:bg-[#27272a]/50'
              }`}
            >
              <User size={16} />
              <span>{isKhmer ? 'គណនី' : 'Profile'}</span>
            </button>

            <button
              onClick={() => setActiveTab('travel')}
              className={`w-full flex items-center space-x-2.5 px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                activeTab === 'travel'
                  ? 'bg-white dark:bg-[#27272a] text-[#003E83] dark:text-[#60a5fa] shadow-xs font-semibold'
                  : 'text-[#6b7280] dark:text-[#a1a1aa] hover:bg-slate-100 dark:hover:bg-[#27272a]/50'
              }`}
            >
              <MapPin size={16} />
              <span>{isKhmer ? 'ចំណូលចិត្ត' : 'Travel Style'}</span>
            </button>
          </div>

          {/* Tab Views */}
          <div className="flex-1 overflow-y-auto p-5 space-y-6">
            
            {/* General Tab */}
            {activeTab === 'general' && (
              <div className="space-y-5">
                <div>
                  <label className="block text-xs font-semibold text-[#111827] dark:text-[#f4f4f5] mb-2">
                    {isKhmer ? 'ស្បែកចំណុចប្រទាក់ (Theme)' : 'Interface Theme'}
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      onClick={() => { if (isDarkMode) toggleTheme(); }}
                      className={`flex items-center space-x-3 p-3 rounded-xl border transition-all ${
                        !isDarkMode
                          ? 'border-[#003E83] dark:border-[#2563eb] bg-blue-50/50 dark:bg-blue-950/30 text-[#003E83] dark:text-[#60a5fa] font-semibold'
                          : 'border-[#f3f4f6] dark:border-[#27272a] text-[#6b7280] dark:text-[#a1a1aa] hover:bg-slate-50 dark:hover:bg-[#27272a]'
                      }`}
                    >
                      <Sun size={18} className="text-amber-500" />
                      <span className="text-xs">{isKhmer ? 'Light Mode' : 'Light Mode'}</span>
                    </button>
                    <button
                      onClick={() => { if (!isDarkMode) toggleTheme(); }}
                      className={`flex items-center space-x-3 p-3 rounded-xl border transition-all ${
                        isDarkMode
                          ? 'border-[#003E83] dark:border-[#2563eb] bg-blue-50/50 dark:bg-blue-950/30 text-[#003E83] dark:text-[#60a5fa] font-semibold'
                          : 'border-[#f3f4f6] dark:border-[#27272a] text-[#6b7280] dark:text-[#a1a1aa] hover:bg-slate-50 dark:hover:bg-[#27272a]'
                      }`}
                    >
                      <Moon size={18} className="text-indigo-400" />
                      <span className="text-xs">{isKhmer ? 'Dark Mode' : 'Dark Mode'}</span>
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-[#111827] dark:text-[#f4f4f5] mb-2">
                    {isKhmer ? 'ភាសាប្រើប្រាស់' : 'Language'}
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      onClick={() => setLanguage('en')}
                      className={`flex items-center justify-between p-3 rounded-xl border transition-all ${
                        language === 'en'
                          ? 'border-[#003E83] dark:border-[#2563eb] bg-blue-50/50 dark:bg-blue-950/30 text-[#003E83] dark:text-[#60a5fa] font-semibold'
                          : 'border-[#f3f4f6] dark:border-[#27272a] text-[#6b7280] dark:text-[#a1a1aa] hover:bg-slate-50 dark:hover:bg-[#27272a]'
                      }`}
                    >
                      <div className="flex items-center space-x-2">
                        <span>🇬🇧</span>
                        <span className="text-xs">English</span>
                      </div>
                      {language === 'en' && <Check size={16} />}
                    </button>
                    <button
                      onClick={() => setLanguage('km')}
                      className={`flex items-center justify-between p-3 rounded-xl border transition-all ${
                        language === 'km'
                          ? 'border-[#003E83] dark:border-[#2563eb] bg-blue-50/50 dark:bg-blue-950/30 text-[#003E83] dark:text-[#60a5fa] font-semibold'
                          : 'border-[#f3f4f6] dark:border-[#27272a] text-[#6b7280] dark:text-[#a1a1aa] hover:bg-slate-50 dark:hover:bg-[#27272a]'
                      }`}
                    >
                      <div className="flex items-center space-x-2">
                        <span>🇰🇭</span>
                        <span className="text-xs">ភាសាខ្មែរ (Khmer)</span>
                      </div>
                      {language === 'km' && <Check size={16} />}
                    </button>
                  </div>
                </div>

                <div className="pt-2 border-t border-[#f3f4f6] dark:border-[#27272a]">
                  <div className="flex items-center space-x-2 text-xs text-[#6b7280] dark:text-[#a1a1aa]">
                    <ShieldCheck size={16} className="text-blue-500" />
                    <span>{isKhmer ? 'ប្រព័ន្ធ AI ដំណើរការដោយសុវត្ថិភាព និងភាពត្រឹមត្រូវ' : 'Powered by Verified Cambodia Tourism Knowledge Base'}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Profile Tab */}
            {activeTab === 'profile' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-[#111827] dark:text-[#f4f4f5] mb-1.5">
                    {isKhmer ? 'ឈ្មោះអ្នកប្រើប្រាស់' : 'Display Name'}
                  </label>
                  <input
                    type="text"
                    value={userProfile.name || ''}
                    onChange={(e) => setUserProfile({ ...userProfile, name: e.target.value })}
                    className="w-full p-2.5 text-xs bg-slate-50 dark:bg-[#18181b] border border-[#e5e7eb] dark:border-[#27272a] rounded-xl text-[#111827] dark:text-[#f4f4f5] focus:outline-none focus:border-[#003E83]"
                    placeholder={isKhmer ? 'បញ្ចូលឈ្មោះរបស់អ្នក...' : 'Enter your name...'}
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-[#111827] dark:text-[#f4f4f5] mb-1.5">
                    {isKhmer ? 'អាសយដ្ឋានអ៊ីមែល (មិនបាច់បំពេញ)' : 'Email (Optional)'}
                  </label>
                  <input
                    type="email"
                    value={userProfile.email || ''}
                    onChange={(e) => setUserProfile({ ...userProfile, email: e.target.value })}
                    className="w-full p-2.5 text-xs bg-slate-50 dark:bg-[#18181b] border border-[#e5e7eb] dark:border-[#27272a] rounded-xl text-[#111827] dark:text-[#f4f4f5] focus:outline-none focus:border-[#003E83]"
                    placeholder="user@example.com"
                  />
                </div>
              </div>
            )}

            {/* Travel Style Tab */}
            {activeTab === 'travel' && (
              <div className="space-y-5">
                <div>
                  <label className="block text-xs font-semibold text-[#111827] dark:text-[#f4f4f5] mb-2">
                    {isKhmer ? 'រៀបចំស្ទីលនៃការដើរលេង' : 'Travel Style'}
                  </label>
                  <div className="grid grid-cols-2 gap-2.5">
                    {travelStyles.map((style) => {
                      const isSelected = userProfile.travelStyle === style.id;
                      return (
                        <button
                          key={style.id}
                          onClick={() => setTravelStyle(style.id)}
                          className={`p-3 text-left rounded-xl border text-xs transition-all ${
                            isSelected
                              ? 'border-[#003E83] dark:border-[#2563eb] bg-blue-50/50 dark:bg-blue-950/30 text-[#003E83] dark:text-[#60a5fa] font-semibold'
                              : 'border-[#f3f4f6] dark:border-[#27272a] text-[#6b7280] dark:text-[#a1a1aa] hover:bg-slate-50 dark:hover:bg-[#27272a]'
                          }`}
                        >
                          {isKhmer ? style.nameKm : style.nameEn}
                        </button>
                      );
                    })}
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-[#111827] dark:text-[#f4f4f5] mb-2">
                    {isKhmer ? 'ខេត្ត/ក្រុងដែលចង់ទៅកម្សាន្ត' : 'Preferred Cambodian Destinations'}
                  </label>
                  <div className="grid grid-cols-2 gap-2.5">
                    {destinations.map((dest) => {
                      const isSelected = (userProfile.preferredDestinations || []).includes(dest.id);
                      return (
                        <button
                          key={dest.id}
                          onClick={() => toggleDestination(dest.id)}
                          className={`p-3 text-left rounded-xl border text-xs transition-all flex items-center justify-between ${
                            isSelected
                              ? 'border-[#003E83] dark:border-[#2563eb] bg-blue-50/50 dark:bg-blue-950/30 text-[#003E83] dark:text-[#60a5fa] font-semibold'
                              : 'border-[#f3f4f6] dark:border-[#27272a] text-[#6b7280] dark:text-[#a1a1aa] hover:bg-slate-50 dark:hover:bg-[#27272a]'
                          }`}
                        >
                          <span>{isKhmer ? dest.nameKm : dest.nameEn}</span>
                          {isSelected && <Check size={14} />}
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

          </div>
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-[#f3f4f6] dark:border-[#27272a] bg-slate-50/50 dark:bg-[#18181b] flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-[#003E83] hover:bg-[#002e62] text-white text-xs font-medium shadow-sm transition-all cursor-pointer"
          >
            {isKhmer ? 'រក្សាទុក' : 'Save Changes'}
          </button>
        </div>

      </div>
    </div>
  );
};

export default SettingsModal;
