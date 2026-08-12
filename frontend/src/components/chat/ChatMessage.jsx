import React, { useState } from 'react';
import { 
  Bot, User, Copy, Check, MapPin, DollarSign, Clock, Star, 
  BarChart3, FileText, Smile, ThumbsUp, ThumbsDown, RotateCcw,
  AlertCircle, Wifi, WifiOff, Sparkles, Image as ImageIcon
} from 'lucide-react';

const ChatMessage = ({ message, language = 'en', onRegenerate }) => {
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState(null); // 'like' | 'dislike' | null
  const isUser = message.sender === 'user' || message.role === 'user';
  const isKhmer = language === 'km';
  const mode = message.mode || 'online';
  const textContent = message.message || message.content || '';

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
      const formattedLine = parts.map((part, pIdx) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return <strong key={pIdx} className="font-bold text-slate-900 dark:text-white">{part.slice(2, -2)}</strong>;
        }
        return part;
      });

      return (
        <span key={lineIdx} className="block mb-1 leading-relaxed">
          {formattedLine}
        </span>
      );
    });
  };

  return (
    <div className={`flex items-start space-x-3 mb-6 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
      
      {/* Avatar */}
      <div
        className={`w-9 h-9 rounded-2xl flex items-center justify-center shrink-0 shadow-sm ${
          isUser
            ? 'bg-[#003E83] text-white'
            : 'bg-[#003E83] text-white shadow-sm'
        }`}
      >
        {isUser ? <User size={18} /> : <Sparkles size={18} />}
      </div>

      {/* Message Content Area */}
      <div className={`max-w-[85%] sm:max-w-[80%] group relative ${isUser ? 'items-end' : 'items-start'}`}>
        
        {/* Mode Tag Badge for AI */}
        {!isUser && (
          <div className="flex items-center space-x-2 mb-1.5 px-1 text-[11px]">
            <span className="font-semibold text-slate-900 dark:text-white">Cambodia Tourism AI</span>
            <span>•</span>
            {mode === 'offline' ? (
              <span className="inline-flex items-center gap-1 font-medium px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700">
                <WifiOff size={10} /> Offline Data
              </span>
            ) : mode === 'fallback' ? (
              <span className="inline-flex items-center gap-1 font-medium px-2 py-0.5 rounded-full bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/60">
                <AlertCircle size={10} /> Local Fallback
              </span>
            ) : (
              <span className="inline-flex items-center gap-1 font-medium px-2 py-0.5 rounded-full bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60">
                <Wifi size={10} /> Online AI
              </span>
            )}
          </div>
        )}

        {/* Message Bubble Container */}
        <div
          className={`px-4 py-3.5 rounded-2xl shadow-2xs text-sm ${
            isUser
              ? 'bg-[#003E83] text-white rounded-tr-xs font-medium'
              : 'bg-white dark:bg-[#18181b] text-[#111827] dark:text-[#f4f4f5] border border-[#f3f4f6] dark:border-[#27272a] rounded-tl-xs'
          }`}
        >
          {/* User Attached Files/Images Preview */}
          {isUser && message.attachments && message.attachments.length > 0 && (
            <div className="mb-2 flex flex-wrap gap-2">
              {message.attachments.map((att, i) => (
                <div key={i} className="flex items-center space-x-1.5 bg-white/20 px-2.5 py-1 rounded-lg text-xs">
                  <ImageIcon size={13} />
                  <span className="truncate max-w-[120px]">{att.name}</span>
                </div>
              ))}
            </div>
          )}

          {formatText(textContent)}

          {/* Structured Analysis Section */}
          {!isUser && message.analysis && (
            <div className="mt-4 p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-700 space-y-3">
              <div className="flex items-center space-x-2 text-[#003E83] dark:text-[#2563eb] font-bold text-xs uppercase tracking-wider">
                <BarChart3 size={15} />
                <span>{isKhmer ? '📊 ការវិភាគទេសចរណ៍' : '📊 Tourism Analysis'}</span>
              </div>
              <p className="text-xs text-slate-700 dark:text-slate-200 leading-relaxed">{message.analysis.overview}</p>
              
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
            </div>
          )}

          {/* Render Rich Cards for Database Sources */}
          {!isUser && message.sources && message.sources.length > 0 && (
            <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 space-y-2.5">
              <p className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
                {isKhmer ? 'ព័ត៌មានពីប្រភពទិន្នន័យ៖' : 'Matched Cambodia Tourism Database Sources:'}
              </p>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {message.sources.map((src, idx) => (
                  <div
                    key={idx}
                    className="bg-slate-50/80 dark:bg-slate-900/70 border border-slate-200 dark:border-slate-700 rounded-xl p-3 hover:border-[#14B8A6] dark:hover:border-[#14B8A6] transition-colors"
                  >
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <h4 className="font-bold text-slate-900 dark:text-white text-xs truncate">
                        {src.name}
                      </h4>
                      {src.type && (
                        <span className="bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full shrink-0">
                          {src.type}
                        </span>
                      )}
                    </div>
                    {src.location && (
                      <div className="flex items-center text-[11px] text-slate-500 dark:text-slate-400 mb-1">
                        <MapPin size={12} className="text-[#003E83] dark:text-[#2563eb] mr-1 shrink-0" />
                        <span className="truncate">{src.location}</span>
                      </div>
                    )}
                    {src.entrance_fee && (
                      <div className="flex items-center text-[11px] text-slate-600 dark:text-slate-300 mb-1">
                        <DollarSign size={12} className="text-blue-600 dark:text-blue-400 mr-1 shrink-0" />
                        <span>{src.entrance_fee}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Message Actions Toolbar (Copy / Regenerate / Thumbs Up / Thumbs Down) */}
        {!isUser && (
          <div className="flex items-center space-x-1 mt-2 text-slate-400 dark:text-slate-500">
            {/* Copy Button */}
            <button
              onClick={handleCopy}
              className="flex items-center space-x-1 p-1.5 rounded-lg hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer text-xs"
              title={copied ? "Copied!" : "Copy response"}
            >
              {copied ? (
                <>
                  <Check size={14} className="text-blue-500" />
                  <span className="text-blue-600 dark:text-blue-400 text-[11px] font-semibold">{isKhmer ? 'បានចម្លង' : 'Copied'}</span>
                </>
              ) : (
                <Copy size={14} />
              )}
            </button>

            {/* Regenerate Button */}
            {onRegenerate && (
              <button
                onClick={onRegenerate}
                className="p-1.5 rounded-lg hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                title="Regenerate response"
              >
                <RotateCcw size={14} />
              </button>
            )}

            {/* Like Button */}
            <button
              onClick={() => handleFeedback('like')}
              className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                feedback === 'like'
                  ? 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/40'
                  : 'hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
              title="Good response"
            >
              <ThumbsUp size={14} />
            </button>

            {/* Dislike Button */}
            <button
              onClick={() => handleFeedback('dislike')}
              className={`p-1.5 rounded-lg transition-colors cursor-pointer ${
                feedback === 'dislike'
                  ? 'text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40'
                  : 'hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
              title="Poor response"
            >
              <ThumbsDown size={14} />
            </button>
          </div>
        )}

      </div>
    </div>
  );
};

export default ChatMessage;
