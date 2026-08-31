<template>
  <div
    v-if="itinerary && itinerary.days && itinerary.days.length > 0"
    class="mt-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xs overflow-hidden text-slate-800 dark:text-slate-100 w-full"
  >
    <!-- Compact Header Bar -->
    <div className="px-3 py-2 bg-gradient-to-r from-blue-500/10 via-transparent to-transparent dark:from-blue-900/20 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between gap-2">
      <div class="flex items-center space-x-1.5 min-w-0">
        <Sparkles :size="13" class="text-[#003E83] dark:text-blue-400 shrink-0" />
        <span class="font-bold text-xs text-slate-900 dark:text-white truncate">
          {{ itinerary.title }}
        </span>
        <span class="text-[11px] text-slate-400 dark:text-slate-500 shrink-0">
          ({{ itinerary.duration_days }}d • {{ itinerary.destination }})
        </span>
      </div>

      <!-- Copy Button -->
      <button
        @click="handleCopyItinerary"
        class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-[10px] font-semibold text-slate-700 dark:text-slate-300 transition-colors cursor-pointer shrink-0"
      >
        <Check v-if="copied" :size="11" class="text-emerald-500" />
        <Copy v-else :size="11" />
        <span>{{ copied ? (isKhmer ? 'បានចម្លង' : 'Copied') : (isKhmer ? 'ចម្លង' : 'Copy') }}</span>
      </button>
    </div>

    <!-- 3-Day Sweet Spot Recommendation Banner (if >3 days) -->
    <div
      v-if="itinerary.duration_days > 3 && itinerary.recommendation_note"
      class="px-3 py-1 bg-amber-50/70 dark:bg-amber-950/30 border-b border-amber-100 dark:border-amber-900/40 flex items-center gap-1.5 text-[10px] text-amber-800 dark:text-amber-300"
    >
      <Star :size="11" class="fill-amber-500 text-amber-500 shrink-0" />
      <span class="truncate">{{ itinerary.recommendation_note }}</span>
    </div>

    <!-- Day Selector Mini-Tabs with horizontal scroll for up to 10+ days -->
    <div class="flex px-2 py-1 bg-slate-50/70 dark:bg-slate-950/40 border-b border-slate-100 dark:border-slate-800/80 gap-1 overflow-x-auto scrollbar-none">
      <button
        v-for="d in itinerary.days"
        :key="d.day"
        @click="activeDay = d.day"
        :class="[
          'px-2.5 py-0.5 rounded-lg text-[11px] font-bold transition-all cursor-pointer shrink-0',
          activeDay === d.day
            ? 'bg-[#003E83] text-white'
            : 'text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800'
        ]"
      >
        {{ isKhmer ? `ថ្ងៃ ${d.day}` : `Day ${d.day}` }}
      </button>
    </div>

    <!-- Compact Activities List: Max 4 Cards -->
    <div class="p-2.5 space-y-1.5">
      <div
        v-if="currentDayData.theme"
        class="text-[11px] font-semibold text-[#003E83] dark:text-blue-400 flex items-center gap-1 mb-1"
      >
        <Calendar :size="11" />
        <span class="truncate">{{ currentDayData.theme }}</span>
      </div>

      <div class="space-y-1.5">
        <div
          v-for="(act, idx) in (currentDayData.activities || []).slice(0, 4)"
          :key="idx"
          class="p-2 rounded-lg bg-slate-50/60 dark:bg-slate-800/30 border border-slate-100 dark:border-slate-800/60 text-xs"
        >
          <div class="flex items-center justify-between gap-1 mb-0.5">
            <span class="font-bold text-[11px] text-slate-900 dark:text-white truncate">
              {{ act.time }} — {{ act.title }}
            </span>
            <span
              v-if="act.transport"
              class="text-[9px] px-1.5 py-0.2 rounded bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-300 shrink-0 font-medium"
            >
              {{ act.transport }}
            </span>
          </div>
          <p class="text-[11px] text-slate-600 dark:text-slate-300 leading-snug line-clamp-2">
            {{ act.description }}
          </p>
          <div
            v-if="act.cost"
            class="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium mt-0.5"
          >
            Est: {{ act.cost }}
          </div>
        </div>
      </div>
    </div>

    <!-- Mini Budget Footer -->
    <div
      v-if="itinerary.formatted_total_budget"
      class="px-3 py-1.5 bg-slate-50 dark:bg-slate-950/70 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-[11px]"
    >
      <span class="text-slate-500 font-medium">{{ isKhmer ? 'ថវិកាប៉ាន់ស្មាន៖' : 'Estimated Budget:' }}</span>
      <span class="font-extrabold text-emerald-600 dark:text-emerald-400">{{ itinerary.formatted_total_budget }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { Calendar, Clock, Navigation, Copy, Check, Sparkles, Star, DollarSign } from 'lucide-vue-next';

const props = defineProps({
  itinerary: {
    type: Object,
    default: null,
  },
  language: {
    type: String,
    default: 'en',
  },
});

const activeDay = ref(1);
const copied = ref(false);
const isKhmer = computed(() => props.language === 'km');

const currentDayData = computed(() => {
  if (!props.itinerary || !props.itinerary.days) return {};
  return props.itinerary.days.find(d => d.day === activeDay.value) || props.itinerary.days[0] || {};
});

const handleCopyItinerary = (e) => {
  e.stopPropagation();
  if (!props.itinerary) return;

  let text = `${props.itinerary.title}\nDestination: ${props.itinerary.destination}\nDuration: ${props.itinerary.duration_days} Days\n\n`;
  (props.itinerary.days || []).forEach(d => {
    text += `DAY ${d.day}: ${d.theme || d.location}\n`;
    (d.activities || []).forEach(act => {
      text += `  • ${act.time} — ${act.title} (${act.transport || 'Transit'})\n    ${act.description}\n`;
    });
    text += '\n';
  });
  if (props.itinerary.formatted_total_budget) {
    text += `Estimated Total Budget: ${props.itinerary.formatted_total_budget}\n`;
  }

  navigator.clipboard.writeText(text);
  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 2000);
};
</script>
