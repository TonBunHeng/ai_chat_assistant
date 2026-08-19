import React, { useState, useRef, useEffect } from 'react';
import { Plus, ArrowUp, X, Image as ImageIcon } from 'lucide-react';

const ChatInput = ({ onSendMessage, isLoading, language = 'en', isCentered = false }) => {
  const [text, setText] = useState('');
  const [attachments, setAttachments] = useState([]);
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);
  const isKhmer = language === 'km';

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 140)}px`;
    }
  }, [text]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if ((!text.trim() && attachments.length === 0) || isLoading) return;
    
    onSendMessage(text.trim(), attachments);
    setText('');
    setAttachments([]);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;
    
    const filePreviews = files.map((file) => ({
      name: file.name,
      size: (file.size / 1024).toFixed(1) + ' KB',
      type: file.type,
      url: URL.createObjectURL(file)
    }));
    
    setAttachments((prev) => [...prev, ...filePreviews]);
  };

  const removeAttachment = (index) => {
    setAttachments((prev) => prev.filter((_, i) => i !== index));
  };

  const hasContent = Boolean(text.trim() || attachments.length > 0);

  return (
    <div className={`w-full ${isCentered ? 'px-2 py-0' : 'bg-[#f8fafc] dark:bg-[#18181b] py-2 px-3 sm:px-4 sticky bottom-0 z-20'}`}>
      <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
        
        {/* Solid ChatGPT Pill-Shaped Input Box (No Blur / No Heavy Shadow) */}
        <div className="relative bg-white dark:bg-[#212121] border border-slate-300 dark:border-zinc-700 focus-within:border-slate-500 dark:focus-within:border-zinc-500 rounded-full px-3.5 py-1.5 sm:py-2 transition-colors">
          
          {/* Attached Files/Images Preview Chips */}
          {attachments.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-2 px-1 pt-1">
              {attachments.map((att, idx) => (
                <div
                  key={idx}
                  className="flex items-center space-x-1.5 bg-slate-100 dark:bg-zinc-800 border border-slate-200 dark:border-zinc-700 px-2.5 py-1 rounded-full text-xs text-slate-800 dark:text-slate-200"
                >
                  <ImageIcon size={13} className="text-[#2563eb]" />
                  <span className="truncate max-w-[120px] font-medium">{att.name}</span>
                  <button
                    type="button"
                    onClick={() => removeAttachment(idx)}
                    className="text-slate-400 hover:text-rose-500 p-0.5 rounded-full transition-colors cursor-pointer"
                  >
                    <X size={12} />
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Controls Row */}
          <div className="flex items-center space-x-1.5 sm:space-x-2">
            
            {/* Hidden File Input */}
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              multiple
              accept="image/*,.pdf,.doc,.docx"
              className="hidden"
            />

            {/* Plus / Attach Button (ChatGPT Style) */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              className="w-8 h-8 rounded-full flex items-center justify-center text-slate-500 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-zinc-800 transition-colors shrink-0 cursor-pointer"
              title={isKhmer ? 'ភ្ជាប់ឯកសារ ឬរូបភាព' : 'Add attachment'}
            >
              <Plus size={18} />
            </button>

            {/* Main Textarea */}
            <textarea
              ref={textareaRef}
              rows={1}
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                isKhmer
                  ? 'សួរអ្វីមួយអំពីកម្ពុជា...'
                  : 'Ask something about Cambodia.'
              }
              disabled={isLoading}
              className="w-full bg-transparent text-xs sm:text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-zinc-400 focus:outline-none resize-none px-1 py-1 max-h-32 min-h-[28px] leading-normal"
            />

            {/* Arrow-Up Send Button (Always Shown) */}
            <button
              type="submit"
              disabled={(!text.trim() && attachments.length === 0) || isLoading}
              className={`w-8 h-8 rounded-full bg-[#2563eb] hover:bg-[#1d4ed8] text-white flex items-center justify-center shrink-0 shadow-xs transition-all duration-150 active:scale-95 ${
                hasContent && !isLoading ? 'opacity-100 cursor-pointer' : 'opacity-40 cursor-not-allowed'
              }`}
              aria-label="Send message"
            >
              <ArrowUp size={17} strokeWidth={2.5} />
            </button>

          </div>
        </div>

        {/* Footer Disclaimer (Only if bottom pinned) */}
        {!isCentered && (
          <p className="text-[11px] text-center text-slate-400 dark:text-zinc-500 mt-2">
            {isKhmer
              ? 'Angkor Verse AI ផ្តល់ព័ត៌មានផ្អែកលើទិន្នន័យទេសចរណ៍ផ្លូវការ'
              : 'Angkor Verse AI can make mistakes. Check important info.'}
          </p>
        )}
      </form>
    </div>
  );
};

export default ChatInput;
