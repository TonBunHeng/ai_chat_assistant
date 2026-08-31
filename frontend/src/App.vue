<template>
  <div class="min-h-screen bg-[#f8fafc] dark:bg-[#18181b] text-zinc-900 dark:text-zinc-100 transition-colors duration-200">
    <RouterView />
  </div>
</template>

<script setup>
import { useTheme } from './composables/useTheme';

// Initialize theme listener and root DOM styling
useTheme();
</script>
