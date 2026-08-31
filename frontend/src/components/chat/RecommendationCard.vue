<template>
  <div v-if="recommendations && recommendations.length > 0" class="mt-2.5 space-y-1.5 w-full">
    <div class="flex items-center space-x-1 text-[11px] font-bold text-[#003E83] dark:text-blue-400 uppercase tracking-wider">
      <Sparkles :size="12" />
      <span>{{ isKhmer ? '✨ គោលដៅណែនាំ' : '✨ Recommended Destinations' }}</span>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
      <div
        v-for="(rec, idx) in recommendations.slice(0, 3)"
        :key="idx"
        class="rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-2.5 shadow-2xs hover:border-blue-300 dark:hover:border-blue-700 transition-all flex flex-col justify-between"
      >
        <div>
          <div class="flex items-center justify-between gap-1 mb-1">
            <h4 class="font-bold text-xs text-slate-900 dark:text-white truncate">
              {{ isKhmer && rec.name_km ? rec.name_km : rec.name }}
            </h4>
            <span
              v-if="rec.match_score"
              class="inline-flex items-center gap-0.5 px-1.5 py-0.2 rounded-full bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 font-extrabold text-[10px] shrink-0"
            >
              <Star :size="9" class="fill-emerald-500 text-emerald-500" />
              {{ rec.match_score }}%
            </span>
          </div>

          <div class="flex items-center text-[10px] text-slate-500 dark:text-slate-400 mb-1">
            <MapPin :size="10" class="text-[#003E83] dark:text-blue-400 mr-0.5 shrink-0" />
            <span class="truncate">{{ rec.province }}</span>
          </div>

          <p class="text-[11px] text-slate-600 dark:text-slate-300 line-clamp-1 leading-snug mb-1">
            {{ isKhmer && rec.description_km ? rec.description_km : rec.description }}
          </p>
        </div>

        <div class="pt-1.5 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between gap-1 text-[10px]">
          <span class="font-medium text-slate-700 dark:text-slate-300">
            {{ rec.price || (rec.estimated_cost_usd === 0 ? 'Free' : `$${rec.estimated_cost_usd}`) }}
          </span>

          <a
            v-if="rec.google_maps_url"
            :href="rec.google_maps_url"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center gap-0.5 font-bold text-[#003E83] dark:text-blue-400 hover:underline"
          >
            <span>{{ isKhmer ? 'ផែនទី' : 'Maps' }}</span>
            <ExternalLink :size="9" />
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { MapPin, DollarSign, Star, ExternalLink, Sparkles } from 'lucide-vue-next';

const props = defineProps({
  recommendations: {
    type: Array,
    default: () => [],
  },
  language: {
    type: String,
    default: 'en',
  },
});

const isKhmer = computed(() => props.language === 'km');
</script>
