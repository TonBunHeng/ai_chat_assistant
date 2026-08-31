<template>
  <div
    v-if="weather && weather.current"
    class="mt-2.5 rounded-xl bg-gradient-to-br from-blue-50/70 via-white to-slate-50 dark:from-slate-900 dark:via-slate-900 dark:to-slate-950 border border-blue-100 dark:border-slate-800 p-2.5 shadow-2xs w-full"
  >
    <!-- Top Row: Province, Condition & Temp -->
    <div class="flex items-center justify-between gap-2 mb-2">
      <div class="flex items-center space-x-1.5">
        <component :is="weatherIcon" :size="18" :class="weatherIconColor" />
        <div>
          <h4 class="font-bold text-xs text-slate-900 dark:text-white">
            {{ weather.province }} {{ weather.province_km ? `(${weather.province_km})` : '' }}
          </h4>
          <span class="text-[10px] text-slate-500">
            {{ isKhmer ? weather.current.condition_km : weather.current.condition }}
          </span>
        </div>
      </div>

      <div class="text-right">
        <span class="text-lg font-black text-[#003E83] dark:text-blue-400">
          {{ weather.current.temperature_c }}°C
        </span>
        <span class="text-[10px] text-slate-400 block -mt-1">
          {{ weather.current.temperature_f }}°F
        </span>
      </div>
    </div>

    <!-- Mini Stats Pill Bar -->
    <div class="flex items-center justify-around py-1 px-2 rounded-lg bg-white/80 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800/80 mb-2 text-[10px]">
      <div class="flex items-center gap-1 text-slate-600 dark:text-slate-300">
        <CloudRain :size="10" class="text-blue-500" />
        <span>{{ weather.current.rain_probability || 20 }}% {{ isKhmer ? 'ភ្លៀង' : 'rain' }}</span>
      </div>
      <div class="flex items-center gap-1 text-slate-600 dark:text-slate-300">
        <Droplets :size="10" class="text-blue-400" />
        <span>{{ weather.current.humidity_percent || 70 }}% {{ isKhmer ? 'សំណើម' : 'humidity' }}</span>
      </div>
      <div class="flex items-center gap-1 text-slate-600 dark:text-slate-300">
        <Wind :size="10" class="text-teal-500" />
        <span>{{ weather.current.wind_speed_kmh || 10 }} km/h</span>
      </div>
    </div>

    <!-- Compact Advice -->
    <div
      v-if="weather.travel_suitability || weather.travel_advice_en || weather.travel_advice_km"
      class="p-1.5 rounded-lg bg-blue-50/70 dark:bg-blue-950/40 border border-blue-100 dark:border-blue-900/50 flex items-start gap-1.5 text-[11px]"
    >
      <ShieldCheck :size="13" class="text-[#003E83] dark:text-blue-400 shrink-0 mt-0.5" />
      <p class="text-slate-700 dark:text-slate-300 text-[10px] leading-tight">
        <strong class="text-[#003E83] dark:text-blue-300">{{ weather.travel_suitability }}:</strong>
        {{ isKhmer ? (weather.travel_advice_km || weather.travel_advice_en) : (weather.travel_advice_en || weather.travel_advice_km) }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { CloudRain, Sun, Cloud, Droplets, Wind, ShieldCheck } from 'lucide-vue-next';

const props = defineProps({
  weather: {
    type: Object,
    default: null,
  },
  language: {
    type: String,
    default: 'en',
  },
});

const isKhmer = computed(() => props.language === 'km');

const weatherIcon = computed(() => {
  const cond = (props.weather?.current?.condition || '').toLowerCase();
  if (cond.includes('rain') || cond.includes('drizzle') || cond.includes('shower')) return CloudRain;
  if (cond.includes('clear') || cond.includes('sun')) return Sun;
  return Cloud;
});

const weatherIconColor = computed(() => {
  const cond = (props.weather?.current?.condition || '').toLowerCase();
  if (cond.includes('rain') || cond.includes('drizzle') || cond.includes('shower')) return 'text-blue-500';
  if (cond.includes('clear') || cond.includes('sun')) return 'text-amber-500';
  return 'text-slate-400';
});
</script>
