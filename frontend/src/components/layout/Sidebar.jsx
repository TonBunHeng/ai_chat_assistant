import React, { useState } from 'react';
import { 
  Plus, MessageSquare, Trash2, MapPin, Hotel, Utensils, Calendar, 
  ChevronRight, Sparkles, HelpCircle, X, AlertTriangle, CheckCircle2 
} from 'lucide-react';

const Sidebar = ({
  sessions = [],
  currentSessionId,
  onSelectSession,
  onNewChat,
  onClearChat,
  onDeleteSession,
  onQuickQuery,
  language = 'en',
  isOpen,
  setIsOpen
}) => {
  const isKhmer = language === 'km';

  // Centered Popup Delete Form Modal State (Select 1 or ALL)
  const [deleteModal, setDeleteModal] = useState({
    isOpen: false,
    deleteScope: 'ONE', // 'ONE' or 'ALL'
    selectedSessionId: ''
  });

  // Open modal when clicking Clear Chat button or single trash icon
  const openDeleteModal = (targetId = null) => {
    const initialId = targetId || currentSessionId || (sessions[0]?.session_id || '');
    setDeleteModal({
      isOpen: true,
      deleteScope: targetId ? 'ONE' : 'ONE',
      selectedSessionId: initialId
    });
  };

  const openDeleteSingleModal = (e, sessionId) => {
    e.stopPropagation();
    openDeleteModal(sessionId);
  };

  const handleConfirmDelete = () => {
    if (deleteModal.deleteScope === 'ALL') {
      if (onClearChat) onClearChat();
    } else if (deleteModal.deleteScope === 'ONE' && deleteModal.selectedSessionId && onDeleteSession) {
      onDeleteSession(deleteModal.selectedSessionId);
    }
    setDeleteModal({ isOpen: false, deleteScope: 'ONE', selectedSessionId: '' });
  };

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40 md:hidden transition-opacity"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed md:static inset-y-0 left-0 z-40 w-72 bg-white dark:bg-[#1E293B] border-r border-[#E2E8F0] dark:border-slate-800 flex flex-col transition-all duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        {/* New Chat Button */}
        <div className="p-4 border-b border-slate-100 dark:border-slate-800">
          <button
            onClick={() => {
              onNewChat();
              setIsOpen(false);
            }}
            className="w-full flex items-center justify-center space-x-2 bg-gradient-to-r from-[#0F766E] to-[#14B8A6] hover:opacity-95 text-white font-medium py-3 px-4 rounded-xl shadow-sm transition-all active:scale-[0.99] cursor-pointer"
          >
            <Plus size={20} />
            <span>{isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat'}</span>
          </button>
        </div>

        {/* Explore Categories Shortcuts */}
        <div className="px-4 py-3 border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/40">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-2 px-1">
            {isKhmer ? 'ស្វែងរកព័ត៌មាន' : 'Explore Cambodia'}
          </p>
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => {
                onQuickQuery(isKhmer ? 'តើមានកន្លែងដើរលេងណាខ្លះនៅសៀមរាប?' : 'Best places in Siem Reap');
                setIsOpen(false);
              }}
              className="flex items-center space-x-2 text-xs font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-[#0F766E] dark:hover:border-[#14B8A6] hover:text-[#0F766E] dark:hover:text-[#14B8A6] transition-colors cursor-pointer"
            >
              <MapPin size={14} className="text-[#0F766E] dark:text-[#14B8A6]" />
              <span className="truncate">{isKhmer ? 'កន្លែងដើរលេង' : 'Places'}</span>
            </button>
            <button
              onClick={() => {
                onQuickQuery(isKhmer ? 'តើមានសណ្ឋាគារណាខ្លះនៅសៀមរាប?' : 'Hotels in Siem Reap');
                setIsOpen(false);
              }}
              className="flex items-center space-x-2 text-xs font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-[#0F766E] dark:hover:border-[#14B8A6] hover:text-[#0F766E] dark:hover:text-[#14B8A6] transition-colors cursor-pointer"
            >
              <Hotel size={14} className="text-[#14B8A6]" />
              <span className="truncate">{isKhmer ? 'សណ្ឋាគារ' : 'Hotels'}</span>
            </button>
            <button
              onClick={() => {
                onQuickQuery(isKhmer ? 'ណែនាំហាងអាហារខ្មែរឆ្ងាញ់ៗ' : 'Best Cambodian food');
                setIsOpen(false);
              }}
              className="flex items-center space-x-2 text-xs font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-[#0F766E] dark:hover:border-[#14B8A6] hover:text-[#0F766E] dark:hover:text-[#14B8A6] transition-colors cursor-pointer"
            >
              <Utensils size={14} className="text-amber-500" />
              <span className="truncate">{isKhmer ? 'ម្ហូបអាហារ' : 'Food'}</span>
            </button>
            <button
              onClick={() => {
                onQuickQuery(isKhmer ? 'បង្កើតគម្រោងដើរលេង ២ថ្ងៃ នៅសៀមរាប' : 'Create a 2-day Cambodia trip');
                setIsOpen(false);
              }}
              className="flex items-center space-x-2 text-xs font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-[#0F766E] dark:hover:border-[#14B8A6] hover:text-[#0F766E] dark:hover:text-[#14B8A6] transition-colors cursor-pointer"
            >
              <Calendar size={14} className="text-purple-500" />
              <span className="truncate">{isKhmer ? 'គម្រោងដើរលេង' : '2-Day Trip'}</span>
            </button>
          </div>
        </div>

        {/* Chat Sessions History List */}
        <div className="flex-1 overflow-y-auto p-3 space-y-1">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 px-2 py-1">
            {isKhmer ? 'ប្រវត្តិសន្ទនា' : 'Chat History'}
          </p>

          {(!Array.isArray(sessions) || sessions.length === 0) ? (
            <div className="text-center py-8 px-4">
              <MessageSquare size={32} className="mx-auto text-slate-300 dark:text-slate-600 mb-2" />
              <p className="text-xs text-slate-400 dark:text-slate-500">
                {isKhmer ? 'មិនទាន់មានប្រវត្តិសន្ទនានៅឡើយទេ' : 'No chat history yet'}
              </p>
            </div>
          ) : (
            (Array.isArray(sessions) ? sessions : []).map((sess, idx) => {
              if (!sess) return null;
              const sid = sess.session_id || `sess_${idx}`;
              const isActive = sid === currentSessionId;
              
              // Extract clean user message title
              let rawTitle = sess.title;
              if (!rawTitle || rawTitle.startsWith('Chat Session #')) {
                if (sess.messages && sess.messages.length > 0) {
                  const firstUserMsg = sess.messages.find(m => m.sender === 'user' || m.role === 'user');
                  rawTitle = firstUserMsg ? (firstUserMsg.message || firstUserMsg.content) : (sess.messages[0].message || sess.messages[0].content);
                }
              }
              
              const displayTitle = (rawTitle && !rawTitle.startsWith('Chat Session #'))
                ? rawTitle.trim()
                : (isKhmer ? 'ការសន្ទនាថ្មី' : 'New Chat');

              return (
                <div
                  key={sid}
                  onClick={() => {
                    if (sess.session_id) onSelectSession(sess.session_id);
                    setIsOpen(false);
                  }}
                  className={`group relative flex items-center justify-between p-2.5 rounded-xl cursor-pointer text-xs transition-all ${
                    isActive
                      ? 'bg-[#0F766E]/10 dark:bg-[#0F766E]/20 text-[#0F766E] dark:text-[#14B8A6] font-medium border border-[#0F766E]/20 dark:border-[#0F766E]/40'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
                  }`}
                  title={displayTitle}
                >
                  <div className="flex items-center space-x-2.5 truncate pr-6">
                    <MessageSquare size={16} className={isActive ? 'text-[#0F766E] dark:text-[#14B8A6]' : 'text-slate-400 dark:text-slate-500'} />
                    <span className="truncate max-w-[175px]">{displayTitle}</span>
                  </div>

                  <div className="flex items-center space-x-1">
                    {/* Delete Individual Session Icon Button */}
                    <button
                      onClick={(e) => openDeleteSingleModal(e, sess.session_id)}
                      title={isKhmer ? 'លុបការសន្ទនានេះ' : 'Delete chat'}
                      className="opacity-0 group-hover:opacity-100 p-1 rounded-lg text-slate-400 dark:text-slate-500 hover:text-rose-600 dark:hover:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-all cursor-pointer"
                    >
                      <Trash2 size={14} />
                    </button>
                    {isActive && (
                      <ChevronRight size={14} className="text-[#0F766E] dark:text-[#14B8A6]" />
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer / Clear Chat Button */}
        <div className="p-3 border-t border-slate-100 dark:border-slate-800 bg-slate-50/80 dark:bg-slate-900/60 flex items-center justify-between">
          <button
            onClick={() => openDeleteModal()}
            className="flex items-center space-x-1.5 text-xs text-rose-600 dark:text-rose-400 hover:text-rose-700 dark:hover:text-rose-300 hover:bg-rose-50 dark:hover:bg-rose-950/40 p-2 rounded-lg font-medium transition-colors cursor-pointer"
          >
            <Trash2 size={15} />
            <span>{isKhmer ? 'លុបការសន្ទនា' : 'Clear Chat'}</span>
          </button>
          
          <span className="text-[11px] text-slate-400 dark:text-slate-500">v1.0.0</span>
        </div>
      </aside>

      {/* Centered Form Popup Modal with Blurred Background (Select 1 or ALL) */}
      {deleteModal.isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 dark:bg-slate-950/70 backdrop-blur-md animate-fade-in">
          <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-100 dark:border-slate-800 max-w-md w-full p-6 transform transition-all animate-in fade-in zoom-in-95 duration-200 relative">
            
            {/* Close Button */}
            <button
              onClick={() => setDeleteModal({ isOpen: false, deleteScope: 'ONE', selectedSessionId: '' })}
              className="absolute top-4 right-4 text-slate-400 dark:text-slate-500 hover:text-slate-600 dark:hover:text-slate-300 p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              <X size={18} />
            </button>

            {/* Header Icon & Title */}
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-rose-100 dark:bg-rose-950/60 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0">
                <Trash2 size={20} />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  {isKhmer ? 'ជម្រើសលុបការសន្ទនា' : 'Delete Chat Options'}
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  {isKhmer ? 'សូមជ្រើសរើសដើម្បីលុប ១ ការសន្ទនា ឬ ទាំងអស់' : 'Select whether to delete 1 chat or all chat history.'}
                </p>
              </div>
            </div>

            {/* Form Selection Options */}
            <div className="space-y-3 mb-6">
              
              {/* Option 1: Delete 1 Session */}
              <label
                onClick={() => setDeleteModal(prev => ({ ...prev, deleteScope: 'ONE' }))}
                className={`flex items-start p-3.5 rounded-xl border cursor-pointer transition-all ${
                  deleteModal.deleteScope === 'ONE'
                    ? 'border-[#0F766E] dark:border-[#14B8A6] bg-teal-50/40 dark:bg-teal-950/30 text-slate-900 dark:text-white ring-1 ring-[#0F766E] dark:ring-[#14B8A6]'
                    : 'border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/60 text-slate-700 dark:text-slate-300'
                }`}
              >
                <input
                  type="radio"
                  name="deleteScope"
                  checked={deleteModal.deleteScope === 'ONE'}
                  onChange={() => setDeleteModal(prev => ({ ...prev, deleteScope: 'ONE' }))}
                  className="mt-0.5 text-[#0F766E] focus:ring-[#0F766E]"
                />
                <div className="ml-3 flex-1">
                  <span className="block text-xs font-bold text-slate-900 dark:text-white">
                    {isKhmer ? 'លុប 1 ការសន្ទនា (Delete 1 Chat)' : 'Delete 1 Chat Session'}
                  </span>
                  <span className="block text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                    {isKhmer ? 'លុបតែប្រវត្តិសន្ទនា ១ ដែលបានជ្រើសរើស' : 'Remove only a single selected chat session'}
                  </span>

                  {/* Dropdown list to pick which 1 chat session to delete */}
                  {deleteModal.deleteScope === 'ONE' && (
                    <div className="mt-2.5">
                      <label className="block text-[10px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">
                        {isKhmer ? 'ជ្រើសរើសការសន្ទនា៖' : 'Select Chat:'}
                      </label>
                      <select
                        value={deleteModal.selectedSessionId}
                        onChange={(e) => setDeleteModal(prev => ({ ...prev, selectedSessionId: e.target.value }))}
                        className="w-full p-2 text-xs bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg focus:outline-none focus:border-[#0F766E] text-slate-800 dark:text-slate-200 font-medium"
                      >
                        {(!Array.isArray(sessions) || sessions.length === 0) ? (
                          <option value="">{isKhmer ? 'គ្មានប្រវត្តិសន្ទនា' : 'No chats available'}</option>
                        ) : (
                          sessions.map((s, i) => {
                            const label = (s.messages && s.messages.length > 0)
                              ? (s.messages[0].message || s.messages[0].content)
                              : (s.title || `Chat Session #${s.session_id || i + 1}`);
                            return (
                              <option key={s.session_id || i} value={s.session_id}>
                                {label.length > 40 ? label.substring(0, 40) + '...' : label}
                              </option>
                            );
                          })
                        )}
                      </select>
                    </div>
                  )}
                </div>
              </label>

              {/* Option 2: Delete All Sessions */}
              <label
                onClick={() => setDeleteModal(prev => ({ ...prev, deleteScope: 'ALL' }))}
                className={`flex items-start p-3.5 rounded-xl border cursor-pointer transition-all ${
                  deleteModal.deleteScope === 'ALL'
                    ? 'border-rose-500 bg-rose-50/40 dark:bg-rose-950/30 text-slate-900 dark:text-white ring-1 ring-rose-500'
                    : 'border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/60 text-slate-700 dark:text-slate-300'
                }`}
              >
                <input
                  type="radio"
                  name="deleteScope"
                  checked={deleteModal.deleteScope === 'ALL'}
                  onChange={() => setDeleteModal(prev => ({ ...prev, deleteScope: 'ALL' }))}
                  className="mt-0.5 text-rose-600 focus:ring-rose-500"
                />
                <div className="ml-3">
                  <span className="block text-xs font-bold text-rose-700 dark:text-rose-400">
                    {isKhmer ? 'លុបការសន្ទនាទាំងអស់ (Delete All Chats)' : 'Delete All Chat Sessions'}
                  </span>
                  <span className="block text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                    {isKhmer ? 'លុបប្រវត្តិសន្ទនាទាំងអស់ដែលបានរក្សាទុកជាអចិន្ត្រៃយ៍' : 'Permanently remove all saved chat sessions'}
                  </span>
                </div>
              </label>

            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-3 pt-2 border-t border-slate-100 dark:border-slate-800">
              <button
                onClick={() => setDeleteModal({ isOpen: false, deleteScope: 'ONE', selectedSessionId: '' })}
                className="flex-1 py-2.5 px-4 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 font-medium text-xs transition-colors cursor-pointer"
              >
                {isKhmer ? 'បោះបង់' : 'Cancel'}
              </button>
              <button
                onClick={handleConfirmDelete}
                disabled={deleteModal.deleteScope === 'ONE' && !deleteModal.selectedSessionId}
                className="flex-1 py-2.5 px-4 rounded-xl bg-rose-600 hover:bg-rose-700 disabled:bg-slate-300 dark:disabled:bg-slate-800 text-white font-medium text-xs shadow-md shadow-rose-600/20 transition-all active:scale-[0.98] cursor-pointer"
              >
                {isKhmer ? 'លុបដែលបានជ្រើស' : 'Confirm Delete'}
              </button>
            </div>

          </div>
        </div>
      )}
    </>
  );
};

export default Sidebar;
