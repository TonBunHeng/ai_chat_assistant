<template>
  <div v-if="place" class="mt-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-3 shadow-2xs w-full">
    <div class="flex items-center justify-between gap-1 mb-1">
      <h4 class="font-bold text-xs text-slate-900 dark:text-white truncate">
        {{ isKhmer && place.name_km ? place.name_km : (place.name || place.title) }}
      </h4>
      <span
        v-if="place.category || place.type"
        class="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[9px] uppercase font-semibold px-2 py-0.5 rounded-md shrink-0"
      >
        {{ place.category || place.type }}
      </span>
    </div>

    <div v-if="place.province || place.location" class="flex items-center text-[10px] text-slate-500 dark:text-slate-400 mb-1">
      <MapPin :size="10" class="text-[#003E83] dark:text-blue-400 mr-1 shrink-0" />
      <span class="truncate">{{ place.province || place.location }}</span>
    </div>

    <p v-if="place.description || place.description_km" class="text-[11px] text-slate-600 dark:text-slate-300 leading-snug line-clamp-2 mb-2">
      {{ isKhmer && place.description_km ? place.description_km : place.description }}
    </p>

    <div class="flex items-center justify-between pt-1.5 border-t border-slate-100 dark:border-slate-800 text-[10px]">
      <span v-if="place.price || place.ticket_price" class="font-medium text-slate-700 dark:text-slate-300">
        {{ place.price || place.ticket_price }}
      </span>
      <span v-else class="text-slate-400">
        {{ isKhmer ? 'ទេសចរណ៍' : 'Attraction' }}
      </span>

      <a
        v-if="place.google_maps_url || place.maps_url"
        :href="place.google_maps_url || place.maps_url"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center gap-0.5 font-bold text-[#003E83] dark:text-blue-400 hover:underline"
      >
        <span>{{ isKhmer ? 'មើលផែនទី' : 'Maps' }}</span>
        <ExternalLink :size="9" />
      </a>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { MapPin, ExternalLink } from 'lucide-vue-next';

const props = defineProps({
  place: {
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
