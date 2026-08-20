import React, { useState } from 'react';
import { Calendar, Clock, Navigation, Copy, Check, Sparkles, Star, DollarSign } from 'lucide-react';

const ItineraryCard = ({ itinerary, language = 'en' }) => {
  const [activeDay, setActiveDay] = useState(1);
  const [copied, setCopied] = useState(false);
  const isKhmer = language === 'km';

  if (!itinerary || !itinerary.days || itinerary.days.length === 0) return null;

  const currentDayData = itinerary.days.find(d => d.day === activeDay) || itinerary.days[0];

  const handleCopyItinerary = (e) => {
    e.stopPropagation();
    let text = `${itinerary.title}\nDestination: ${itinerary.destination}\nDuration: ${itinerary.duration_days} Days\n\n`;
    itinerary.days.forEach(d => {
      text += `DAY ${d.day}: ${d.theme || d.location}\n`;
      (d.activities || []).forEach(act => {
        text += `  • ${act.time} — ${act.title} (${act.transport || 'Transit'})\n    ${act.description}\n`;
      });
      text += '\n';
    });
    if (itinerary.formatted_total_budget) {
      text += `Estimated Total Budget: ${itinerary.formatted_total_budget}\n`;
    }
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="mt-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xs overflow-hidden text-slate-800 dark:text-slate-100 w-full">
      {/* Compact Header Bar */}
      <div className="px-3 py-2 bg-gradient-to-r from-blue-500/10 via-transparent to-transparent dark:from-blue-900/20 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between gap-2">
        <div className="flex items-center space-x-1.5 min-w-0">
          <Sparkles size={13} className="text-[#003E83] dark:text-blue-400 shrink-0" />
          <span className="font-bold text-xs text-slate-900 dark:text-white truncate">
            {itinerary.title}
          </span>
          <span className="text-[11px] text-slate-400 dark:text-slate-500 shrink-0">
            ({itinerary.duration_days}d • {itinerary.destination})
          </span>
        </div>

        {/* Copy Button */}
        <button
          onClick={handleCopyItinerary}
          className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-[10px] font-semibold text-slate-700 dark:text-slate-300 transition-colors cursor-pointer shrink-0"
        >
          {copied ? <Check size={11} className="text-emerald-500" /> : <Copy size={11} />}
          <span>{copied ? (isKhmer ? 'បានចម្លង' : 'Copied') : (isKhmer ? 'ចម្លង' : 'Copy')}</span>
        </button>
      </div>

      {/* 3-Day Sweet Spot Recommendation Banner (if >3 days) */}
      {itinerary.duration_days > 3 && itinerary.recommendation_note && (
        <div className="px-3 py-1 bg-amber-50/70 dark:bg-amber-950/30 border-b border-amber-100 dark:border-amber-900/40 flex items-center gap-1.5 text-[10px] text-amber-800 dark:text-amber-300">
          <Star size={11} className="fill-amber-500 text-amber-500 shrink-0" />
          <span className="truncate">{itinerary.recommendation_note}</span>
        </div>
      )}

      {/* Day Selector Mini-Tabs with horizontal scroll for up to 10+ days */}
      <div className="flex px-2 py-1 bg-slate-50/70 dark:bg-slate-950/40 border-b border-slate-100 dark:border-slate-800/80 gap-1 overflow-x-auto scrollbar-none">
        {itinerary.days.map((d) => (
          <button
            key={d.day}
            onClick={() => setActiveDay(d.day)}
            className={`px-2.5 py-0.5 rounded-lg text-[11px] font-bold transition-all cursor-pointer shrink-0 ${
              activeDay === d.day
                ? 'bg-[#003E83] text-white'
                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800'
            }`}
          >
            {isKhmer ? `ថ្ងៃ ${d.day}` : `Day ${d.day}`}
          </button>
        ))}
      </div>

      {/* Compact Activities List: Max 4 Cards */}
      <div className="p-2.5 space-y-1.5">
        {currentDayData.theme && (
          <div className="text-[11px] font-semibold text-[#003E83] dark:text-blue-400 flex items-center gap-1 mb-1">
            <Calendar size={11} />
            <span className="truncate">{currentDayData.theme}</span>
          </div>
        )}

        <div className="space-y-1.5">
          {(currentDayData.activities || []).slice(0, 4).map((act, idx) => (
            <div
              key={idx}
              className="p-2 rounded-lg bg-slate-50/60 dark:bg-slate-800/30 border border-slate-100 dark:border-slate-800/60 text-xs"
            >
              <div className="flex items-center justify-between gap-1 mb-0.5">
                <span className="font-bold text-[11px] text-slate-900 dark:text-white truncate">
                  {act.time} — {act.title}
                </span>
                {act.transport && (
                  <span className="text-[9px] px-1.5 py-0.2 rounded bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-300 shrink-0 font-medium">
                    {act.transport}
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-600 dark:text-slate-300 leading-snug line-clamp-2">
                {act.description}
              </p>
              {act.cost && (
                <div className="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium mt-0.5">
                  Est: {act.cost}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Mini Budget Footer */}
      {itinerary.formatted_total_budget && (
        <div className="px-3 py-1.5 bg-slate-50 dark:bg-slate-950/70 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-[11px]">
          <span className="text-slate-500 font-medium">{isKhmer ? 'ថវិកាប៉ាន់ស្មាន៖' : 'Estimated Budget:'}</span>
          <span className="font-extrabold text-emerald-600 dark:text-emerald-400">{itinerary.formatted_total_budget}</span>
        </div>
      )}
    </div>
  );
};

export default ItineraryCard;
