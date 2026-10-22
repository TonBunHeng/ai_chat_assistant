<template>
  <header class="bg-white/95 dark:bg-[#18181b]/95 backdrop-blur-md border-b border-zinc-200/80 dark:border-zinc-800/80 sticky top-0 z-30 transition-colors duration-200">
    <div class="w-full px-3 sm:px-4 h-13 flex items-center justify-between gap-2">

      <!-- Left Side: Sidebar Toggle & Brand -->
      <div class="flex items-center space-x-2 shrink-0 min-w-0">
        <!-- Sidebar Toggle Icon -->
        <button
          type="button"
          @click="$emit('toggle-sidebar')"
          class="w-8 h-8 rounded-lg flex items-center justify-center text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors cursor-pointer"
          :title="isKhmer ? 'បិទ/បើក របារចំហៀង' : 'Toggle Sidebar'"
        >
          <PanelLeftOpen v-if="!sidebarOpen" :size="17" />
          <PanelLeftClose v-else :size="17" />
        </button>

        <div class="flex items-center space-x-2 shrink-0">
          <div class="w-7 h-7 rounded-lg bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 flex items-center justify-center font-bold text-xs shadow-2xs">
            🇰🇭
          </div>
          <div class="flex items-center space-x-2">
            <span class="font-bold text-sm sm:text-base tracking-tight text-zinc-900 dark:text-white block">
              Cambodia Super AI
            </span>
            <span class="hidden md:inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-medium bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700">
              Gemini & RAG
            </span>
          </div>
        </div>
      </div>

      <!-- Right Side: Controls & Actions -->
      <div class="flex items-center space-x-1.5 sm:space-x-2 shrink-0">

        <!-- Status Indicator Badge -->
        <div class="hidden sm:flex items-center">
          <div
            v-if="!isOnline || mode === 'offline' || mode === 'degraded' || mode === 'fallback'"
            class="flex items-center space-x-1.5 h-7 px-2.5 rounded-full bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 text-[11px] font-medium"
            title="Running in local offline mode"
          >
            <WifiOff :size="11" />
            <span>Offline</span>
          </div>
          <div
            v-else
            class="flex items-center space-x-1.5 h-7 px-2.5 rounded-full bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200/80 dark:border-emerald-800/60 text-emerald-700 dark:text-emerald-300 text-[11px] font-medium"
            title="Online Cloud Intelligence"
          >
            <span class="relative flex h-1.5 w-1.5">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-1.5 w-1.5 bg-emerald-500"></span>
            </span>
            <span>Online</span>
          </div>
        </div>

        <!-- Language Switcher Pill -->
        <button
          type="button"
          @click="$emit('toggle-language')"
          class="h-7 px-2.5 rounded-full bg-zinc-100 hover:bg-zinc-200/80 dark:bg-zinc-800 dark:hover:bg-zinc-700 border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 text-[11px] font-semibold transition-colors cursor-pointer"
          :title="isKhmer ? 'ប្តូរទៅភាសាអង់គ្លេស' : 'Switch to Khmer'"
        >
          {{ isKhmer ? 'English' : 'ភាសាខ្មែរ' }}
        </button>

        <!-- Theme Toggle -->
        <button
          type="button"
          @click="toggleTheme"
          class="w-7 h-7 rounded-full flex items-center justify-center bg-zinc-100 hover:bg-zinc-200/80 dark:bg-zinc-800 dark:hover:bg-zinc-700 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 transition-colors cursor-pointer"
          :title="isDarkMode ? 'Light Mode' : 'Dark Mode'"
        >
          <Sun v-if="isDarkMode" :size="13" class="text-amber-400" />
          <Moon v-else :size="13" />
        </button>

        <!-- Settings Modal Button -->
        <button
          type="button"
          @click="$emit('open-settings')"
          class="w-7 h-7 rounded-full flex items-center justify-center bg-zinc-100 hover:bg-zinc-200/80 dark:bg-zinc-800 dark:hover:bg-zinc-700 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 transition-colors cursor-pointer"
          :title="isKhmer ? 'ការកំណត់' : 'Settings'"
        >
          <Settings :size="13" />
        </button>

      </div>

    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import {
  PanelLeftOpen, PanelLeftClose, WifiOff, Settings, Sun, Moon
} from 'lucide-vue-next';
import { useTheme } from '../../composables/useTheme';

const props = defineProps({
  sidebarOpen: {
    type: Boolean,
    default: true,
  },
  language: {
    type: String,
    default: 'en',
  },
  isOnline: {
    type: Boolean,
    default: true,
  },
  mode: {
    type: String,
    default: 'online',
  },
});

defineEmits(['toggle-sidebar', 'new-chat', 'open-settings', 'toggle-language']);

const { isDarkMode, toggleTheme } = useTheme();

const isKhmer = computed(() => props.language === 'km');
</script>
