<template>
  <div v-if="event" class="mt-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-3 shadow-2xs w-full">
    <div class="flex items-center justify-between gap-1 mb-1">
      <h4 class="font-bold text-xs text-slate-900 dark:text-white truncate">
        {{ isKhmer && event.name_km ? event.name_km : (event.name || event.title) }}
      </h4>
      <span
        v-if="event.category || event.type"
        class="bg-blue-50 dark:bg-blue-950 text-blue-700 dark:text-blue-300 text-[9px] font-semibold px-2 py-0.5 rounded-md shrink-0"
      >
        {{ event.category || event.type }}
      </span>
    </div>

    <div v-if="event.date || event.dates" class="flex items-center text-[10px] text-slate-500 dark:text-slate-400 mb-1">
      <Calendar :size="10" class="text-[#003E83] dark:text-blue-400 mr-1 shrink-0" />
      <span class="truncate">{{ event.date || event.dates }}</span>
    </div>

    <div v-if="event.province || event.location" class="flex items-center text-[10px] text-slate-500 dark:text-slate-400 mb-1">
      <MapPin :size="10" class="text-slate-400 mr-1 shrink-0" />
      <span class="truncate">{{ event.province || event.location }}</span>
    </div>

    <p v-if="event.description || event.description_km" class="text-[11px] text-slate-600 dark:text-slate-300 leading-snug line-clamp-2">
      {{ isKhmer && event.description_km ? event.description_km : event.description }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { Calendar, MapPin } from 'lucide-vue-next';

const props = defineProps({
  event: {
    type: Object,
    default: null,
  },
  language: {
    type: String,
    default: 'en',
  },
});

const isKhmer = computed(() => props.language === 'km');
</script>
