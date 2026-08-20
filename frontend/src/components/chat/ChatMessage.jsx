import React, { useState } from 'react';
import { 
  Bot, User, Copy, Check, MapPin, DollarSign, Clock, Star, 
  BarChart3, FileText, Smile, ThumbsUp, ThumbsDown, RotateCcw,
  AlertCircle, Wifi, WifiOff, Sparkles, Image as ImageIcon, CheckCircle2, ExternalLink
} from 'lucide-react';
import ItineraryCard from './ItineraryCard';
import WeatherCard from './WeatherCard';
import RecommendationCard from './RecommendationCard';

const ChatMessage = ({ message, language = 'en', onRegenerate }) => {
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const isUser = message.sender === 'user' || message.role === 'user';
  const isKhmer = language === 'km';
  const mode = message.mode || 'online';
  const modelName = message.model || (mode === 'offline' ? 'CamTour-On-Mistral-Ai' : 'Gemini Flash');
  const textContent = message.message || message.content || '';
  const hasKhmer = isKhmer || /[\u1780-\u17FF]/.test(textContent);

  const handleCopy = () => {
    navigator.clipboard.writeText(textContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleFeedback = (type) => {
    setFeedback((prev) => (prev === type ? null : type));
  };

  const formatText = (text) => {
    if (!text) return '';
    return text.split('\n').map((line, lineIdx) => {
      const parts = line.split(/(\*\*.*?\*\*)/g);
      const isLineKhmer = /[\u1780-\u17FF]/.test(line);
      const formattedLine = parts.map((part, pIdx) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return <strong key={pIdx} className="font-bold text-slate-900 dark:text-white">{part.slice(2, -2)}</strong>;
        }
        return part;
      });

      return (
        <span key={lineIdx} className={`block mb-1 ${isLineKhmer || hasKhmer ? 'leading-[1.75]' : 'leading-relaxed'}`}>
          {formattedLine}
        </span>
      );
    });
  };

  // Determine if a specialized card is active to avoid showing duplicate source cards
  const hasSpecializedCard = Boolean(message.itinerary || (message.recommendations && message.recommendations.length > 0));

  return (
    <div className={`flex items-start space-x-3 mb-5 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 shadow-xs overflow-hidden ${
          isUser
            ? 'bg-[#003E83] text-white'
            : 'bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700'
        }`}
      >
        {isUser ? (
          <User size={16} />
        ) : (
          <img
            src="/tourism_logo.png"
            alt="Angkor Verse AI"
            className="w-full h-full object-contain p-0.5 rounded-xl"
          />
        )}
      </div>

      {/* Message Content Area */}
      <div className={`max-w-[85%] sm:max-w-[80%] group relative ${isUser ? 'items-end' : 'items-start'}`}>
        
        {/* Mode Tag Badge for AI */}
        {!isUser && (
          <div className="flex flex-wrap items-center gap-1.5 mb-1 px-1 text-[11px]">
            <span className="font-bold text-slate-900 dark:text-white">Angkor Verse AI</span>
            <span>•</span>
            {mode === 'offline' || mode === 'degraded' || mode === 'fallback' ? (
              <span className="inline-flex items-center gap-1 font-medium px-2 py-0.2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700 text-[10px]">
                <WifiOff size={9} /> Offline
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 font-medium px-2 py-0.2 rounded-full bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60 text-[10px]">
                <Wifi size={9} /> Online
              </span>
            )}
          </div>
        )}

        {/* Message Bubble Container */}
        <div
          className={`px-4 py-3 rounded-2xl shadow-2xs text-[15px] sm:text-[15.5px] ${
            hasKhmer ? 'leading-[1.75]' : 'leading-relaxed'
          } ${
            isUser
              ? 'bg-[#003E83] text-white rounded-tr-xs font-medium'
              : 'bg-white dark:bg-[#18181b] text-[#111827] dark:text-[#f4f4f5] border border-[#f3f4f6] dark:border-[#27272a] rounded-tl-xs'
          }`}
        >
          {/* User Attached Files/Images Preview */}
          {isUser && message.attachments && message.attachments.length > 0 && (
            <div className="mb-2 flex flex-wrap gap-1.5">
              {message.attachments.map((att, i) => (
                <div key={i} className="flex items-center space-x-1 bg-white/20 px-2 py-0.5 rounded-md text-xs">
                  <ImageIcon size={12} />
                  <span className="truncate max-w-[120px]">{att.name}</span>
                </div>
              ))}
            </div>
          )}

          {formatText(textContent)}

          {/* Real-time Weather Widget */}
          {!isUser && message.weather && (
            <WeatherCard weather={message.weather} language={language} />
          )}

          {/* Interactive Itinerary Component */}
          {!isUser && message.itinerary && (
            <ItineraryCard itinerary={message.itinerary} language={language} />
          )}

          {/* Smart Recommendation Cards (Only if no itinerary to prevent clutter) */}
          {!isUser && !message.itinerary && message.recommendations && message.recommendations.length > 0 && (
            <RecommendationCard recommendations={message.recommendations} language={language} />
          )}

          {/* Matched Database Source Cards (Only shown if no specialized itinerary/rec card is active) */}
          {!isUser && !hasSpecializedCard && message.sources && message.sources.length > 0 && (
            <div className="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800 space-y-1.5">
              <p className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
                {isKhmer ? 'ប្រភពទិន្នន័យទេសចរណ៍៖' : 'Tourism Database Source:'}
              </p>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {message.sources.slice(0, 2).map((src, idx) => (
                  <div
                    key={idx}
                    className="bg-slate-50/80 dark:bg-slate-900/70 border border-slate-200 dark:border-slate-700 rounded-xl p-2.5 text-xs hover:border-[#003E83] dark:hover:border-blue-500 transition-colors"
                  >
                    <div className="flex items-center justify-between gap-1 mb-1">
                      <h4 className="font-bold text-slate-900 dark:text-white text-xs truncate">
                        {src.name || src.title || 'Cambodia Destination'}
                      </h4>
                      {(src.category || src.type) && (
                        <span className="bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[9px] uppercase font-semibold px-1.5 py-0.2 rounded-md shrink-0">
                          {src.category || src.type}
                        </span>
                      )}
                    </div>
                    {(src.location || src.province) && (
                      <div className="flex items-center text-[10px] text-slate-500 dark:text-slate-400 mb-0.5">
                        <MapPin size={10} className="text-[#003E83] dark:text-[#2563eb] mr-1 shrink-0" />
                        <span className="truncate">{src.location || src.province}</span>
                      </div>
                    )}
                    {src.google_maps_url && (
                      <div className="mt-1 pt-1 border-t border-slate-200/60 dark:border-slate-800 flex justify-end">
                        <a
                          href={src.google_maps_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-0.5 text-[9px] font-bold text-[#003E83] dark:text-blue-400 hover:underline"
                        >
                          <span>{isKhmer ? 'មើលផែនទី' : 'Maps'}</span>
                          <ExternalLink size={8} />
                        </a>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Message Actions Toolbar */}
        {!isUser && (
          <div className="flex items-center space-x-1 mt-1 text-slate-400 dark:text-slate-500">
            <button
              onClick={handleCopy}
              className="flex items-center space-x-1 p-1 rounded-md hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer text-xs"
              title={copied ? "Copied!" : "Copy response"}
            >
              {copied ? (
                <>
                  <Check size={12} className="text-blue-500" />
                  <span className="text-blue-600 dark:text-blue-400 text-[10px] font-semibold">{isKhmer ? 'បានចម្លង' : 'Copied'}</span>
                </>
              ) : (
                <Copy size={12} />
              )}
            </button>

            {onRegenerate && (
              <button
                onClick={onRegenerate}
                className="p-1 rounded-md hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                title="Regenerate response"
              >
                <RotateCcw size={12} />
              </button>
            )}

            <button
              onClick={() => handleFeedback('like')}
              className={`p-1 rounded-md transition-colors cursor-pointer ${
                feedback === 'like'
                  ? 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/40'
                  : 'hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
              title="Good response"
            >
              <ThumbsUp size={12} />
            </button>

            <button
              onClick={() => handleFeedback('dislike')}
              className={`p-1 rounded-md transition-colors cursor-pointer ${
                feedback === 'dislike'
                  ? 'text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40'
                  : 'hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
              title="Poor response"
            >
              <ThumbsDown size={12} />
            </button>
          </div>
        )}

      </div>
    </div>
  );
};

export default ChatMessage;
