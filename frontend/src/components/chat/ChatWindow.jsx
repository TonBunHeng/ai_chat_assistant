import React, { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import TypingIndicator from './TypingIndicator';
import { 
  Bot, Compass, Sparkles, MapPin, Utensils, Hotel, Calendar, 
  HelpCircle, AlertCircle 
} from 'lucide-react';

const ChatWindow = ({
  messages = [],
  isLoading = false,
  error = null,
  onSendMessage,
  language = 'en'
}) => {
  const messagesEndRef = useRef(null);
  const isKhmer = language === 'km';

  // Auto-scroll to bottom of chat on new messages or typing indicator
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Prompt suggestions specified in the requirement
  const suggestionsEn = [
    { text: "Tell me about Angkor Wat", icon: <Compass size={18} className="text-[#0F766E]" /> },
    { text: "Best places in Siem Reap", icon: <MapPin size={18} className="text-[#14B8A6]" /> },
    { text: "Best Cambodian food", icon: <Utensils size={18} className="text-amber-500" /> },
    { text: "Hotels in Siem Reap", icon: <Hotel size={18} className="text-emerald-600" /> },
    { text: "Things to do in Phnom Penh", icon: <Sparkles size={18} className="text-purple-500" /> },
    { text: "Create a 2-day Cambodia trip", icon: <Calendar size={18} className="text-blue-500" /> },
  ];

  const suggestionsKm = [
    { text: "ប្រាប់ខ្ញុំអំពីប្រាសាទអង្គរវត្ត", icon: <Compass size={18} className="text-[#0F766E]" /> },
    { text: "តំបន់ទេសចរណ៍ល្អៗនៅសៀមរាប", icon: <MapPin size={18} className="text-[#14B8A6]" /> },
    { text: "ម្ហូបអាហារខ្មែរឆ្ងាញ់ៗប្រចាំតំបន់", icon: <Utensils size={18} className="text-amber-500" /> },
    { text: "សណ្ឋាគារល្អៗនៅខេត្តសៀមរាប", icon: <Hotel size={18} className="text-emerald-600" /> },
    { text: "កន្លែងដើរលេងនៅរាជធានីភ្នំពេញ", icon: <Sparkles size={18} className="text-purple-500" /> },
    { text: "បង្កើតគម្រោងដើរលេង ២ថ្ងៃ នៅកម្ពុជា", icon: <Calendar size={18} className="text-blue-500" /> },
  ];

  const suggestions = isKhmer ? suggestionsKm : suggestionsEn;

  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-6 bg-[#F8FAFC] dark:bg-[#0F172A] transition-colors duration-200">
      <div className="max-w-4xl mx-auto">
        
        {/* Empty State / Welcome Hero */}
        {messages.length === 0 ? (
          <div className="py-8 sm:py-12 px-4 text-center animate-fade-in">
            {/* Hero Icon */}
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-[#0F766E] to-[#14B8A6] text-white flex items-center justify-center mx-auto mb-4 shadow-lg shadow-[#0F766E]/20">
              <Bot size={36} />
            </div>

            <h2 className="text-2xl sm:text-3xl font-bold text-[#0F172A] dark:text-white tracking-tight mb-2">
              {isKhmer ? '🤖 សួស្តី! តើខ្ញុំអាចជួយអ្នកទស្សនាកម្ពុជាយ៉ាងដូចម្តេច?' : '🤖 Hello! How can I help you explore Cambodia today?'}
            </h2>
            
            <p className="text-slate-500 dark:text-slate-400 text-sm max-w-lg mx-auto mb-8">
              {isKhmer
                ? 'ខ្ញុំជាជំនួយការ AI ទេសចរណ៍ផ្លូវការ អាចផ្តល់ព័ត៌មានអំពីប្រាសាទបុរាណ សណ្ឋាគារ ហាងអាហារ ព្រឹត្តិការណ៍ និងតម្លៃសំបុត្រ។'
                : 'Your intelligent AI companion for exploring Cambodian heritage, top attractions, hotels, food, events, ticket fees, and travel itineraries.'}
            </p>

            {/* Quick Suggestion Cards */}
            <div className="max-w-2xl mx-auto">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-3">
                {isKhmer ? 'សំណួរដែលគេពេញនិយមសួរ៖' : 'Quick Suggestions:'}
              </p>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
                {suggestions.map((item, idx) => (
                  <button
                    key={idx}
                    onClick={() => onSendMessage(item.text)}
                    className="flex items-center space-x-3 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700/80 border border-[#E2E8F0] dark:border-slate-700 hover:border-[#14B8A6] dark:hover:border-[#14B8A6] p-3.5 rounded-xl shadow-2xs transition-all text-sm font-medium text-slate-700 dark:text-slate-200 hover:text-[#0F766E] dark:hover:text-[#14B8A6] group active:scale-[0.98] cursor-pointer"
                  >
                    <div className="p-2 rounded-lg bg-slate-50 dark:bg-slate-700/50 group-hover:bg-[#14B8A6]/10 dark:group-hover:bg-[#14B8A6]/20 transition-colors">
                      {item.icon}
                    </div>
                    <span className="truncate">{item.text}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          /* Active Chat Messages */
          <div className="space-y-2">
            {messages.map((msg, index) => (
              <ChatMessage key={msg.id || index} message={msg} language={language} />
            ))}
          </div>
        )}

        {/* Typing Indicator */}
        {isLoading && <TypingIndicator language={language} />}

        {/* Error Alert Message */}
        {error && (
          <div className="my-4 p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800/80 text-rose-800 dark:text-rose-300 text-sm flex items-start space-x-3">
            <AlertCircle size={20} className="text-rose-500 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">{isKhmer ? 'មានបញ្ហាក្នុងការតភ្ជាប់' : 'Connection Error'}</p>
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
