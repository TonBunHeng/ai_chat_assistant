import React, { useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import TypingIndicator from './TypingIndicator';
import { 
  Compass, Sparkles, MapPin, Utensils, Hotel, Calendar, 
  HelpCircle, AlertCircle, Sun, Award, Globe, ArrowUpRight
} from 'lucide-react';

const ChatWindow = ({
  messages = [],
  isLoading = false,
  error = null,
  onSendMessage,
  onRegenerate,
  language = 'en'
}) => {
  const messagesEndRef = useRef(null);
  const isKhmer = language === 'km';

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Suggested Prompts explicitly required
  const suggestionsEn = [
    {
      title: "Best Places",
      text: "What are the best places to visit in Cambodia?",
      desc: "Explore top heritage sites, beaches & cities",
      icon: <MapPin size={20} className="text-[#2563eb]" />
    },
    {
      title: "Angkor Wat",
      text: "Tell me about Angkor Wat.",
      desc: "History, ticket prices & best sunrise spots",
      icon: <Compass size={20} className="text-[#003E83]" />
    },
    {
      title: "3-Day Itinerary",
      text: "Create a 3-day Cambodia itinerary.",
      desc: "Day-by-day travel plan for Siem Reap & Phnom Penh",
      icon: <Calendar size={20} className="text-purple-500" />
    },
    {
      title: "Cambodian Food",
      text: "What Cambodian food should I try?",
      desc: "Amok, Lok Lak, street food & best restaurants",
      icon: <Utensils size={20} className="text-amber-500" />
    },
    {
      title: "Best Time to Visit",
      text: "What is the best time to visit Cambodia?",
      desc: "Weather seasons, festivals & travel tips",
      icon: <Sun size={20} className="text-blue-500" />
    }
  ];

  const suggestionsKm = [
    {
      title: "តំបន់ទេសចរណ៍",
      text: "តើមានកន្លែងដើរលេងណាខ្លះដែលល្អបំផុតនៅកម្ពុជា?",
      desc: "ស្វែងរកប្រាសាទបុរាណ ឆ្នេរសមុទ្រ និងក្រុងទេសចរណ៍",
      icon: <MapPin size={20} className="text-[#2563eb]" />
    },
    {
      title: "ប្រាសាទអង្គរវត្ត",
      text: "ប្រាប់ខ្ញុំអំពីប្រាសាទអង្គរវត្ត។",
      desc: "ប្រវត្តិសាស្រ្ត តម្លៃសំបុត្រ និងចំណុចមើលថ្ងៃរះ",
      icon: <Compass size={20} className="text-[#003E83]" />
    },
    {
      title: "គម្រោង ៣ថ្ងៃ",
      text: "បង្កើតគម្រោងដើរលេង ៣ថ្ងៃ នៅកម្ពុជា។",
      desc: "គម្រោងធ្វើដំណើរប្រចាំថ្ងៃនៅសៀមរាប និងភ្នំពេញ",
      icon: <Calendar size={20} className="text-purple-500" />
    },
    {
      title: "ម្ហូបអាហារខ្មែរ",
      text: "តើមានម្ហូបអាហារខ្មែរអ្វីខ្លះដែលខ្ញុំควរសាកល្បង?",
      desc: "អាមុក ឡុកឡាក់ ម្ហូបតាមផ្លូវ និងហាងឆ្ងាញ់ៗ",
      icon: <Utensils size={20} className="text-amber-500" />
    },
    {
      title: "រដូវកាលដើរលេង",
      text: "តើរដូវណាដែលល្អបំផុតសម្រាប់មកទស្សនាកម្ពុជា?",
      desc: "ធាតុអាកាស ពិធីបុណ្យ និងគន្លឹះធ្វើដំណើរ",
      icon: <Sun size={20} className="text-blue-500" />
    }
  ];

  const suggestions = isKhmer ? suggestionsKm : suggestionsEn;

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 sm:p-8 bg-[#f8fafc] dark:bg-[#18181b] transition-colors duration-200">
      <div className="max-w-4xl mx-auto">
        
        {/* Welcome Screen / Hero state */}
        {messages.length === 0 ? (
          <div className="py-6 sm:py-12 px-2 animate-fade-in">
            
            {/* Greeting Header */}
            <div className="mb-8 text-left space-y-2">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-[#003E83]/10 text-[#003E83] dark:text-[#60a5fa] border border-[#003E83]/30 text-xs font-semibold">
                <Sparkles size={14} />
                <span>{isKhmer ? 'ជំនួយការ AI ទេសចរណ៍កម្ពុជា' : 'Cambodia Tourism AI'}</span>
              </div>

              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-[#111827] dark:text-[#f4f4f5] leading-tight">
                {isKhmer ? 'តើខ្ញុំអាចជួយអ្នកទស្សនាកម្ពុជាយ៉ាងដូចម្តេច?' : 'How can I help you explore Cambodia?'}
              </h1>
              
              <p className="text-slate-500 dark:text-slate-400 text-sm max-w-2xl leading-relaxed">
                {isKhmer
                  ? 'សួរអំពីតំបន់បេតិកភណ្ឌពិភពលោក ប្រាសាទបុរាណ ឆ្នេរសមុទ្រ សណ្ឋាគារ ម្ហូបអាហារ និងបង្កើតគម្រោងធ្វើដំណើរផ្ទាល់ខ្លួន។'
                  : 'Ask about World Heritage temples, tropical islands, authentic Khmer cuisine, luxury stays, ticket passes, and custom itineraries.'}
              </p>
            </div>

            {/* Suggested Prompt Cards */}
            <div className="space-y-3 mb-8">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 px-1">
                {isKhmer ? 'សំណួរដែលបានណែនាំ៖' : 'Suggested Prompts:'}
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {suggestions.map((item, idx) => (
                  <button
                    key={idx}
                    onClick={() => onSendMessage(item.text)}
                    className="flex flex-col justify-between bg-white dark:bg-[#18181b] hover:bg-blue-50/40 dark:hover:bg-[#27272a] border border-slate-200/90 dark:border-[#27272a] hover:border-[#003E83] dark:hover:border-[#60a5fa] p-4 rounded-2xl shadow-2xs hover:shadow-md transition-all text-left group active:scale-[0.98] cursor-pointer relative overflow-hidden"
                  >
                    <div className="flex items-center justify-between w-full mb-3">
                      <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-[#27272a] group-hover:bg-[#003E83]/10 transition-colors">
                        {item.icon}
                      </div>
                      <ArrowUpRight size={16} className="text-slate-300 dark:text-slate-600 group-hover:text-[#003E83] dark:group-hover:text-[#60a5fa] transition-colors" />
                    </div>
                    <div>
                      <h4 className="font-bold text-slate-900 dark:text-white text-xs mb-1 group-hover:text-[#003E83] dark:group-hover:text-[#60a5fa] transition-colors">
                        {item.title}
                      </h4>
                      <p className="text-xs text-slate-600 dark:text-slate-300 line-clamp-2 leading-relaxed">
                        {item.text}
                      </p>
                    </div>
                  </button>
                ))}
              </div>
            </div>

          </div>
        ) : (
          /* Active Chat Conversation */
          <div className="space-y-4">
            {messages.map((msg, index) => (
              <ChatMessage
                key={msg.id || index}
                message={msg}
                language={language}
                onRegenerate={onRegenerate}
              />
            ))}
          </div>
        )}

        {/* Loading / Typing Indicator */}
        {isLoading && <TypingIndicator language={language} />}

        {/* Error Alert Box */}
        {error && (
          <div className="my-4 p-4 rounded-2xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800/80 text-rose-800 dark:text-rose-300 text-sm flex items-start space-x-3 shadow-xs">
            <AlertCircle size={20} className="text-rose-500 shrink-0 mt-0.5" />
            <div className="flex-1">
              <p className="font-semibold">{isKhmer ? 'មានបញ្ហាក្នុងការតភ្ជាប់' : 'Connection Warning'}</p>
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
