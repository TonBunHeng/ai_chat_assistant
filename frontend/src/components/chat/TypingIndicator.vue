<template>
  <div class="flex justify-start mb-6 animate-fade-in">
    <!-- Typing Bubble -->
    <div class="bg-white dark:bg-[#18181b] border border-slate-200/90 dark:border-[#27272a] px-4 py-3 rounded-2xl rounded-tl-xs shadow-2xs flex items-center space-x-2.5">
      <span class="text-xs sm:text-[13px] text-slate-500 dark:text-slate-400 font-medium">
        {{ isKhmer ? 'Angkor Verse AI កំពុងគិត...' : 'Angkor Verse AI is thinking' }}
      </span>
      <div class="flex items-center space-x-1">
        <div class="w-2 h-2 rounded-full bg-[#2563eb] typing-dot"></div>
        <div class="w-2 h-2 rounded-full bg-[#003E83] typing-dot"></div>
        <div class="w-2 h-2 rounded-full bg-slate-900 dark:bg-white typing-dot"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  language: {
    type: String,
    default: 'en',
  },
});

const isKhmer = computed(() => props.language === 'km');
</script>
