<template>
  <header class="h-14 shrink-0 bg-white/95 dark:bg-[#18181b]/95 backdrop-blur-md border-b border-zinc-200 dark:border-zinc-800 sticky top-0 z-30 transition-colors duration-200">
    <div class="h-full w-full px-3 sm:px-4 flex items-center justify-between gap-2">

      <!-- Left Section: Sidebar Toggle, Logo & Brand -->
      <div class="flex items-center space-x-2 sm:space-x-3 shrink-0 min-w-0">
        <!-- Sidebar Toggle Button -->
        <button
          type="button"
          @click="$emit('toggle-sidebar')"
          class="w-8 h-8 rounded-lg flex items-center justify-center text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors cursor-pointer shrink-0"
          :title="sidebarOpen ? (isKhmer ? 'បិទរបារចំហៀង' : 'Close Sidebar') : (isKhmer ? 'បើករបារចំហៀង' : 'Open Sidebar')"
        >
          <PanelLeftClose v-if="sidebarOpen" :size="18" />
          <PanelLeftOpen v-else :size="18" />
        </button>

        <!-- Cambodia Super AI Logo & Title -->
        <div class="flex items-center space-x-2 min-w-0">
          <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-zinc-100 dark:bg-zinc-800 border border-zinc-200/80 dark:border-zinc-700/80 flex items-center justify-center shrink-0 overflow-hidden shadow-2xs">
            <img src="/tourism_logo.png" alt="Cambodia AI" class="w-5 h-5 sm:w-6 sm:h-6 object-contain" />
          </div>

          <div class="flex items-center space-x-2 min-w-0">
            <span class="font-bold text-sm sm:text-base tracking-tight text-zinc-900 dark:text-white truncate">
              Cambodia Super AI
            </span>
            <span class="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-medium bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700 shrink-0">
              Gemini & RAG
            </span>
          </div>
        </div>
      </div>

      <!-- Right Section: Status Indicator, Language, Theme & Settings -->
      <div class="flex items-center space-x-1.5 sm:space-x-2 shrink-0">

        <!-- Online Status Indicator (Desktop Pill) -->
        <div class="hidden sm:flex items-center">
          <div
            v-if="!isOnline || mode === 'offline' || mode === 'degraded' || mode === 'fallback'"
            class="flex items-center space-x-1.5 h-8 px-2.5 rounded-full bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 text-xs font-medium shrink-0"
            title="Running in local offline mode"
          >
            <WifiOff :size="12" />
            <span>Offline</span>
          </div>
          <div
            v-else
            class="flex items-center space-x-1.5 h-8 px-2.5 rounded-full bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200/80 dark:border-emerald-800/60 text-emerald-700 dark:text-emerald-300 text-xs font-medium shrink-0"
            title="Online Cloud Intelligence"
          >
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span>Online</span>
          </div>
        </div>

        <!-- Mobile Online Status Indicator Icon -->
        <div
          class="flex sm:hidden items-center justify-center w-8 h-8 rounded-lg bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 shrink-0"
          :title="isOnline ? 'Online' : 'Offline'"
        >
          <span v-if="isOnline && mode !== 'offline'" class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <WifiOff v-else :size="13" class="text-zinc-500 dark:text-zinc-400" />
        </div>

        <!-- Khmer Language Selector -->
        <button
          type="button"
          @click="$emit('toggle-language')"
          class="h-8 px-2.5 rounded-lg bg-zinc-100 hover:bg-zinc-200/80 dark:bg-zinc-800 dark:hover:bg-zinc-700 border border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300 text-xs font-semibold transition-colors cursor-pointer flex items-center space-x-1 shrink-0"
          :title="isKhmer ? 'ប្តូរទៅភាសាអង់គ្លេស' : 'Switch to Khmer'"
        >
          <span>{{ isKhmer ? 'English' : 'ភាសាខ្មែរ' }}</span>
        </button>

        <!-- Dark/Light Theme Toggle -->
        <button
          type="button"
          @click="toggleTheme"
          class="w-8 h-8 rounded-lg flex items-center justify-center bg-zinc-100 hover:bg-zinc-200/80 dark:bg-zinc-800 dark:hover:bg-zinc-700 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 transition-colors cursor-pointer shrink-0"
          :title="isDarkMode ? 'Light Mode' : 'Dark Mode'"
        >
          <Sun v-if="isDarkMode" :size="15" class="text-amber-400" />
          <Moon v-else :size="15" />
        </button>

        <!-- Settings Button -->
        <button
          type="button"
          @click="$emit('open-settings')"
          class="w-8 h-8 rounded-lg flex items-center justify-center bg-zinc-100 hover:bg-zinc-200/80 dark:bg-zinc-800 dark:hover:bg-zinc-700 border border-zinc-200 dark:border-zinc-700 text-zinc-600 dark:text-zinc-300 transition-colors cursor-pointer shrink-0"
          :title="isKhmer ? 'ការកំណត់' : 'Settings'"
        >
          <Settings :size="15" />
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
