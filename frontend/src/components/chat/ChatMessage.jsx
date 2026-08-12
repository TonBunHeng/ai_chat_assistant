import React, { useState } from 'react';
import { 
  Bot, User, Copy, Check, MapPin, DollarSign, Clock, Star, 
  BarChart3, FileText, Smile, ThumbsUp, ThumbsDown, AlertCircle, Wifi, WifiOff 
} from 'lucide-react';

const ChatMessage = ({ message, language = 'en' }) => {
  const [copied, setCopied] = useState(false);
  const isUser = message.sender === 'user' || message.role === 'user';
  const isKhmer = language === 'km';
  const mode = message.mode || 'online';
  const textContent = message.message || message.content || '';

  const handleCopy = () => {
    navigator.clipboard.writeText(textContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatText = (text) => {
    if (!text) return '';
    return text.split('\n').map((line, lineIdx) => {
      const parts = line.split(/(\*\*.*?\*\*)/g);
      const formattedLine = parts.map((part, pIdx) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return <strong key={pIdx} className="font-semibold text-slate-900 dark:text-white">{part.slice(2, -2)}</strong>;
        }
        return part;
      });

      return (
        <span key={lineIdx} className="block mb-1">
          {formattedLine}
        </span>
      );
    });
  };

  return (
    <div className={`flex items-start space-x-3 mb-5 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      
      {/* Avatar */}
      <div
        className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 shadow-xs ${
          isUser
            ? 'bg-slate-800 dark:bg-slate-700 text-white'
            : mode === 'offline'
            ? 'bg-slate-600 dark:bg-slate-700 text-white'
            : mode === 'fallback'
            ? 'bg-amber-600 dark:bg-amber-700 text-white'
            : 'bg-gradient-to-tr from-[#0F766E] to-[#14B8A6] text-white shadow-md shadow-[#0F766E]/20'
        }`}
      >
        {isUser ? <User size={18} /> : <Bot size={20} />}
      </div>

      {/* Message Content Bubble */}
      <div className={`max-w-[85%] sm:max-w-[80%] group relative ${isUser ? 'items-end' : 'items-start'}`}>
        
        {/* Mode Tag Badge */}
        {!isUser && (
          <div className="flex items-center space-x-2 mb-1.5 px-1 text-[11px]">
            {mode === 'offline' ? (
              <span className="inline-flex items-center gap-1 font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                <WifiOff size={10} /> Offline Tourism Data
              </span>
            ) : mode === 'fallback' ? (
              <span className="inline-flex items-center gap-1 font-semibold px-2 py-0.5 rounded-full bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60">
                <AlertCircle size={10} /> Local Fallback Context
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 font-semibold px-2 py-0.5 rounded-full bg-[#14B8A6]/10 text-[#0F766E] dark:text-[#14B8A6] border border-[#14B8A6]/20">
                <Wifi size={10} /> Online AI Engine
              </span>
            )}
          </div>
        )}

        <div
          className={`px-4 py-3.5 rounded-2xl shadow-xs text-sm leading-relaxed ${
            isUser
              ? 'bg-[#0F766E] text-white rounded-tr-xs'
              : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 border border-[#E2E8F0] dark:border-slate-700 rounded-tl-xs'
          }`}
        >
          {formatText(textContent)}

          {/* Structured Analysis Section */}
          {!isUser && message.analysis && (
            <div className="mt-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700 space-y-3">
              <div className="flex items-center space-x-2 text-[#0F766E] dark:text-[#14B8A6] font-bold text-xs uppercase tracking-wider">
                <BarChart3 size={16} />
                <span>{isKhmer ? '📊 ការវិភាគទេសចរណ៍ឆ្លាតវៃ' : '📊 Smart Tourism Analysis'}</span>
              </div>
              <p className="text-xs text-slate-700 dark:text-slate-200 leading-relaxed font-medium">{message.analysis.overview}</p>
              
              {message.analysis.key_findings && (
                <div>
                  <h5 className="font-semibold text-xs text-slate-900 dark:text-white mb-1">{isKhmer ? 'របកគំហើញសំខាន់ៗ៖' : 'Key Findings:'}</h5>
                  <ul className="list-disc list-inside text-xs text-slate-600 dark:text-slate-300 space-y-1">
                    {message.analysis.key_findings.map((kf, i) => (
                      <li key={i}>{kf}</li>
                    ))}
                  </ul>
                </div>
              )}

              {message.analysis.recommendations && (
                <div>
                  <h5 className="font-semibold text-xs text-slate-900 dark:text-white mb-1">{isKhmer ? 'អនុសាសន៍៖' : 'Recommendations:'}</h5>
                  <ul className="list-disc list-inside text-xs text-slate-600 dark:text-slate-300 space-y-1">
                    {message.analysis.recommendations.map((rec, i) => (
                      <li key={i}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}

              {message.analysis.summary && (
                <div className="pt-2 border-t border-slate-200 dark:border-slate-700 text-xs text-slate-700 dark:text-slate-300">
                  <strong>{isKhmer ? 'សេចក្តីសង្ខេប៖' : 'Summary:'}</strong> {message.analysis.summary}
                </div>
              )}
            </div>
          )}

          {/* Structured Summary Section */}
          {!isUser && message.summary && (
            <div className="mt-4 p-4 rounded-xl bg-teal-50/50 dark:bg-teal-950/30 border border-teal-200 dark:border-teal-800/60 space-y-2">
              <div className="flex items-center space-x-2 text-[#0F766E] dark:text-[#14B8A6] font-bold text-xs uppercase tracking-wider">
                <FileText size={16} />
                <span>{isKhmer ? '📝 សេចក្តីសង្ខេបទេសចរណ៍' : '📝 Tourism Summary'}</span>
              </div>
              <p className="text-xs text-slate-700 dark:text-slate-300"><strong>{isKhmer ? 'តំបន់សំខាន់ៗ៖' : 'Attractions:'}</strong> {message.summary.main_attractions}</p>
              <p className="text-xs text-slate-700 dark:text-slate-300"><strong>{isKhmer ? 'ចំណាប់អារម្មណ៍៖' : 'Tourist Interests:'}</strong> {message.summary.tourist_interests}</p>
              <p className="text-xs text-slate-700 dark:text-slate-300"><strong>{isKhmer ? 'ព័ត៌មានសំខាន់៖' : 'Important Info:'}</strong> {message.summary.important_info}</p>
              <p className="text-xs text-[#0F766E] dark:text-[#14B8A6] font-medium pt-1"><strong>{isKhmer ? 'គំនិតចម្បង៖' : 'Key Insight:'}</strong> {message.summary.key_insight}</p>
            </div>
          )}

          {/* Structured Sentiment Analysis Section */}
          {!isUser && message.sentiment && (
            <div className="mt-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700 space-y-3">
              <div className="flex items-center space-x-2 text-[#0F766E] dark:text-[#14B8A6] font-bold text-xs uppercase tracking-wider">
                <Smile size={16} />
                <span>{isKhmer ? '⭐ ការវិភាគមតិភ្ញៀវទេសចរ' : '⭐ Tourist Review Sentiment Analysis'}</span>
              </div>

              {!message.sentiment.has_enough_data ? (
                <p className="text-xs text-slate-500 dark:text-slate-400 italic">{message.sentiment.message}</p>
              ) : (
                <div className="space-y-2">
                  <div className="grid grid-cols-3 gap-2 text-center text-xs">
                    <div className="bg-emerald-50 dark:bg-emerald-950/40 p-2 rounded-lg border border-emerald-200 dark:border-emerald-800/60">
                      <span className="font-bold text-emerald-700 dark:text-emerald-400 block text-base">{message.sentiment.positive_pct}%</span>
                      <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium">Positive</span>
                    </div>
                    <div className="bg-slate-100 dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                      <span className="font-bold text-slate-700 dark:text-slate-300 block text-base">{message.sentiment.neutral_pct}%</span>
                      <span className="text-[10px] text-slate-600 dark:text-slate-400 font-medium">Neutral</span>
                    </div>
                    <div className="bg-rose-50 dark:bg-rose-950/40 p-2 rounded-lg border border-rose-200 dark:border-rose-800/60">
                      <span className="font-bold text-rose-700 dark:text-rose-400 block text-base">{message.sentiment.negative_pct}%</span>
                      <span className="text-[10px] text-rose-600 dark:text-rose-400 font-medium">Negative</span>
                    </div>
                  </div>

                  {message.sentiment.positive_topics && message.sentiment.positive_topics.length > 0 && (
                    <div className="pt-2">
                      <h5 className="text-xs font-semibold text-slate-900 dark:text-white flex items-center gap-1 mb-1">
                        <ThumbsUp size={12} className="text-emerald-600 dark:text-emerald-400" />
                        {isKhmer ? 'ប្រធានបទដែលទទួលបានការសរសើរ៖' : 'Most Positive Topics:'}
                      </h5>
                      <div className="flex flex-wrap gap-1">
                        {message.sentiment.positive_topics.map((tp, i) => (
                          <span key={i} className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-200 font-medium">
                            {tp}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Render Rich Cards for Database Sources */}
          {!isUser && message.sources && message.sources.length > 0 && (
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700 space-y-3">
              <p className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
                {isKhmer ? 'ព័ត៌មានពីប្រភពទិន្នន័យ៖' : 'Matched Database Sources:'}
              </p>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {message.sources.map((src, idx) => (
                  <div
                    key={idx}
                    className="bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700 rounded-xl p-3 hover:border-[#14B8A6] dark:hover:border-[#14B8A6] transition-colors"
                  >
                    <div className="flex items-center justify-between gap-2 mb-1.5">
                      <h4 className="font-bold text-slate-900 dark:text-white text-xs truncate">
                        {src.name}
                      </h4>
                      {src.type && (
                        <span className="bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full shrink-0">
                          {src.type}
                        </span>
                      )}
                    </div>
                    {src.location && (
                      <div className="flex items-center text-[11px] text-slate-500 dark:text-slate-400 mb-1">
                        <MapPin size={12} className="text-[#0F766E] dark:text-[#14B8A6] mr-1 shrink-0" />
                        <span className="truncate">{src.location}</span>
                      </div>
                    )}
                    {src.entrance_fee && (
                      <div className="flex items-center text-[11px] text-slate-600 dark:text-slate-300 mb-1">
                        <DollarSign size={12} className="text-emerald-600 dark:text-emerald-400 mr-1 shrink-0" />
                        <span>{src.entrance_fee}</span>
                      </div>
                    )}
                    {src.opening_hours && (
                      <div className="flex items-center text-[11px] text-slate-500 dark:text-slate-400 mb-1">
                        <Clock size={12} className="text-amber-500 mr-1 shrink-0" />
                        <span>{src.opening_hours}</span>
                      </div>
                    )}
                    {src.rating && (
                      <div className="flex items-center text-[11px] text-amber-600 dark:text-amber-400 font-medium">
                        <Star size={12} className="fill-amber-400 text-amber-400 mr-1 shrink-0" />
                        <span>{src.rating} / 5.0</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Message Controls (Copy / Timestamp) */}
        <div className={`flex items-center space-x-2 mt-1 px-1 text-[11px] text-slate-400 dark:text-slate-500 ${isUser ? 'justify-end' : 'justify-start'}`}>
          <span>{isUser ? (isKhmer ? 'អ្នកប្រើប្រាស់' : 'You') : 'AIChat_Support'}</span>
          <span>•</span>
          <button
            onClick={handleCopy}
            className="hover:text-slate-600 dark:hover:text-slate-300 transition-colors p-1 rounded cursor-pointer"
            title="Copy response"
          >
            {copied ? <Check size={12} className="text-emerald-600 dark:text-emerald-400" /> : <Copy size={12} />}
          </button>
        </div>

      </div>
    </div>
  );
};

export default ChatMessage;
