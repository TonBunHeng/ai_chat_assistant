<template>
  <div class="flex justify-start mb-6 animate-fade-in">
    <!-- Typing Bubble -->
    <div class="bg-white dark:bg-[#18181b] border border-zinc-200 dark:border-zinc-800 px-4 py-3 rounded-2xl rounded-tl-xs shadow-2xs flex items-center space-x-2.5">
      <span class="text-xs sm:text-[13px] text-zinc-500 dark:text-zinc-400 font-medium">
        {{ isKhmer ? 'AngkorVers AI កំពុងគិត...' : 'AngkorVers AI is thinking...' }}
      </span>
      <div class="flex items-center space-x-1">
        <div class="w-1.5 h-1.5 rounded-full bg-zinc-400 dark:bg-zinc-500 typing-dot"></div>
        <div class="w-1.5 h-1.5 rounded-full bg-zinc-600 dark:bg-zinc-400 typing-dot"></div>
        <div class="w-1.5 h-1.5 rounded-full bg-zinc-900 dark:bg-white typing-dot"></div>
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
