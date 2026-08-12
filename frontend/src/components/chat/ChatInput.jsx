import React, { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, X, Image as ImageIcon, Sparkles } from 'lucide-react';

const ChatInput = ({ onSendMessage, isLoading, language = 'en' }) => {
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

  return (
    <div className="bg-[#f8fafc] dark:bg-[#18181b] py-2 px-3 sm:px-4 sticky bottom-0 z-20 transition-colors duration-200">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        
        {/* Gemini-Inspired Compact Floating Composer Box */}
        <div className="relative bg-white dark:bg-[#18181b] border border-[#f3f4f6] dark:border-[#27272a] focus-within:border-[#2563eb] dark:focus-within:border-[#2563eb] focus-within:ring-2 focus-within:ring-[#2563eb]/20 rounded-2xl px-3 py-1.5 shadow-sm transition-all">
          
          {/* Attached Files/Images Preview Chips */}
          {attachments.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-1.5 px-1 pt-1">
              {attachments.map((att, idx) => (
                <div
                  key={idx}
                  className="flex items-center space-x-1.5 bg-slate-100 dark:bg-[#27272a] border border-[#f3f4f6] dark:border-[#27272a] px-2.5 py-1 rounded-lg text-xs text-slate-800 dark:text-slate-200"
                >
                  <ImageIcon size={13} className="text-[#2563eb]" />
                  <span className="truncate max-w-[120px] font-medium">{att.name}</span>
                  <button
                    type="button"
                    onClick={() => removeAttachment(idx)}
                    className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-0.5 rounded-full"
                  >
                    <X size={12} />
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Input & Action Buttons Row */}
          <div className="flex items-center space-x-2">
            
            {/* Hidden File Input */}
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              multiple
              accept="image/*,.pdf,.doc,.docx"
              className="hidden"
            />

            {/* Paperclip Attachment Icon Button */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              className="p-1.5 rounded-xl text-slate-400 dark:text-slate-500 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#27272a] transition-colors shrink-0 cursor-pointer"
              title={isKhmer ? 'ភ្ជាប់រូបភាព ឬ ឯកសារ' : 'Attach images or files'}
            >
              <Paperclip size={18} />
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
                  ? 'សួរអំពីប្រាសាទបុរាណ សណ្ឋាគារ ហាងអាហារកម្ពុជា...'
                  : 'Ask about Cambodia places, hotels, food, travel plans...'
              }
              disabled={isLoading}
              className="w-full bg-transparent text-xs sm:text-sm text-[#111827] dark:text-[#f4f4f5] placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none resize-none px-1 py-1 max-h-32 min-h-[32px] leading-normal"
            />

            {/* Send Button */}
            <button
              type="submit"
              disabled={(!text.trim() && attachments.length === 0) || isLoading}
              className={`p-2 rounded-xl text-white font-medium flex items-center justify-center shrink-0 transition-all ${
                (text.trim() || attachments.length > 0) && !isLoading
                  ? 'bg-[#003E83] hover:bg-[#002e62] shadow-sm active:scale-95 cursor-pointer'
                  : 'bg-slate-200 dark:bg-[#27272a] text-slate-400 dark:text-slate-600 cursor-not-allowed'
              }`}
              aria-label="Send message"
            >
              <Send size={16} />
            </button>
          </div>
        </div>

        {/* Footer Disclaimer */}
        <p className="text-[11px] text-center text-slate-400 dark:text-slate-500 mt-2.5">
          {isKhmer
            ? 'Cambodia Tourism AI ផ្តល់ព័ត៌មានផ្អែកលើទិន្នន័យទេសចរណ៍ផ្លូវការ'
            : 'Cambodia Tourism AI provides verified travel insights grounded in official database context.'}
        </p>
      </form>
    </div>
  );
};

export default ChatInput;
