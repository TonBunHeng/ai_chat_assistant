import React from 'react';
import { CloudRain, Sun, Cloud, Droplets, Wind, ShieldCheck } from 'lucide-react';

const WeatherCard = ({ weather, language = 'en' }) => {
  const isKhmer = language === 'km';
  if (!weather || !weather.current) return null;

  const { current, forecast, province, province_km, travel_suitability, travel_advice_en, travel_advice_km } = weather;

  const getWeatherIcon = (condition = '') => {
    const c = condition.toLowerCase();
    if (c.includes('rain') || c.includes('drizzle') || c.includes('shower')) return <CloudRain className="text-blue-500" size={18} />;
    if (c.includes('clear') || c.includes('sun')) return <Sun className="text-amber-500" size={18} />;
    return <Cloud className="text-slate-400" size={18} />;
  };

  return (
    <div className="mt-2.5 rounded-xl bg-gradient-to-br from-blue-50/70 via-white to-slate-50 dark:from-slate-900 dark:via-slate-900 dark:to-slate-950 border border-blue-100 dark:border-slate-800 p-2.5 shadow-2xs w-full">
      {/* Top Row: Province, Condition & Temp */}
      <div className="flex items-center justify-between gap-2 mb-2">
        <div className="flex items-center space-x-1.5">
          {getWeatherIcon(current.condition)}
          <div>
            <h4 className="font-bold text-xs text-slate-900 dark:text-white">
              {province} {province_km && `(${province_km})`}
            </h4>
            <span className="text-[10px] text-slate-500">
              {isKhmer ? current.condition_km : current.condition}
            </span>
          </div>
        </div>

        <div className="text-right">
          <span className="text-lg font-black text-[#003E83] dark:text-blue-400">
            {current.temperature_c}°C
          </span>
          <span className="text-[10px] text-slate-400 block -mt-1">
            {current.temperature_f}°F
          </span>
        </div>
      </div>

      {/* Mini Stats Pill Bar */}
      <div className="flex items-center justify-around py-1 px-2 rounded-lg bg-white/80 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800/80 mb-2 text-[10px]">
        <div className="flex items-center gap-1 text-slate-600 dark:text-slate-300">
          <CloudRain size={10} className="text-blue-500" />
          <span>{current.rain_probability || 20}% {isKhmer ? 'ភ្លៀង' : 'rain'}</span>
        </div>
        <div className="flex items-center gap-1 text-slate-600 dark:text-slate-300">
          <Droplets size={10} className="text-blue-400" />
          <span>{current.humidity_percent || 70}% {isKhmer ? 'សំណើម' : 'humidity'}</span>
        </div>
        <div className="flex items-center gap-1 text-slate-600 dark:text-slate-300">
          <Wind size={10} className="text-teal-500" />
          <span>{current.wind_speed_kmh || 10} km/h</span>
        </div>
      </div>

      {/* Compact Advice */}
      <div className="p-1.5 rounded-lg bg-blue-50/70 dark:bg-blue-950/40 border border-blue-100 dark:border-blue-900/50 flex items-start gap-1.5 text-[11px]">
        <ShieldCheck size={13} className="text-[#003E83] dark:text-blue-400 shrink-0 mt-0.5" />
        <p className="text-slate-700 dark:text-slate-300 text-[10px] leading-tight">
          <strong className="text-[#003E83] dark:text-blue-300">{travel_suitability}:</strong> {isKhmer ? (travel_advice_km || travel_advice_en) : (travel_advice_en || travel_advice_km)}
        </p>
      </div>
    </div>
  );
};

export default WeatherCard;
