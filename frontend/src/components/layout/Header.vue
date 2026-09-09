<template>
  <header class="bg-white/95 dark:bg-[#18181b]/95 backdrop-blur-md border-b border-slate-100 dark:border-[#27272a] sticky top-0 z-30 transition-colors duration-200">
    <div class="w-full px-3 sm:px-6 h-14 flex items-center justify-between gap-2">

      <!-- Left Side: Brand Logo & Title -->
      <div class="flex items-center space-x-2.5 shrink-0 min-w-0">
        <div class="flex items-center space-x-2 shrink-0">
          <img
            src="/tourism_logo.png"
            alt="Angkor Verse AI Logo"
            width="36"
            height="36"
            style="max-width: 36px; max-height: 36px;"
            class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl object-contain shadow-xs shrink-0"
          />
          <div>
            <span class="font-extrabold text-sm sm:text-base tracking-tight text-slate-900 dark:text-white truncate block">
              Angkor Verse AI
            </span>
            <span class="hidden sm:block text-[10px] text-slate-400 dark:text-slate-500 -mt-0.5">
              Cambodia Tourism Intelligence
            </span>
          </div>
        </div>

        <!-- Model Selector Badge (Desktop) -->
        <div class="hidden lg:flex items-center space-x-1.5 h-7 px-2.5 rounded-full bg-slate-100 dark:bg-[#27272a] border border-slate-200 dark:border-[#27272a] text-slate-700 dark:text-slate-300 text-[11px] font-semibold">
          <Sparkles :size="12" class="text-[#003E83] dark:text-blue-400" />
          <span>Angkor Verse 2.5</span>
        </div>
      </div>

      <!-- Right Side: New Chat, Status Badge & Settings -->
      <div class="flex items-center space-x-2 shrink-0">

        <!-- New Chat Button -->
        <button
          @click="$emit('new-chat')"
          class="relative group overflow-hidden flex items-center space-x-1.5 h-8 px-3.5 rounded-full bg-[#003E83] hover:bg-[#002e62] dark:bg-blue-600 dark:hover:bg-blue-500 text-white text-xs sm:text-[13px] font-semibold shadow-xs shadow-blue-900/20 border border-white/15 cursor-pointer shrink-0 transition-all duration-300 ease-out hover:shadow-md hover:shadow-blue-500/25 active:scale-95"
          :title="isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat'"
        >
          <!-- Smooth Overlay Glow for Buttery-Smooth Color Shifting -->
          <span class="absolute inset-0 bg-gradient-to-r from-blue-500/30 to-indigo-500/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 ease-out pointer-events-none"></span>

          <Plus :size="14" class="relative z-10 shrink-0 stroke-[2.5] transition-transform duration-300 ease-out group-hover:rotate-90" />
          <span class="relative z-10 tracking-tight">{{ isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat' }}</span>
        </button>

        <!-- Status Indicator Badge -->
        <div class="hidden sm:flex items-center">
          <div
            v-if="!isOnline || mode === 'offline' || mode === 'degraded' || mode === 'fallback'"
            class="flex items-center space-x-1.5 h-8 px-3 rounded-full bg-slate-100 dark:bg-slate-800/90 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs font-semibold shadow-2xs transition-colors duration-200"
            title="Running on local offline model & database"
          >
            <WifiOff :size="13" class="text-slate-500" />
            <span>Offline</span>
          </div>

          <div
            v-else
            class="flex items-center space-x-1.5 h-8 px-3 rounded-full bg-emerald-50/90 dark:bg-emerald-950/40 border border-emerald-200/90 dark:border-emerald-800/60 text-emerald-800 dark:text-emerald-300 text-xs font-semibold shadow-2xs transition-colors duration-200"
            title="Connected to Online AI & Real-Time Services"
          >
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span>Online</span>
          </div>
        </div>

        <!-- Settings Modal Launcher Button -->
        <button
          @click="$emit('open-settings')"
          class="w-8 h-8 rounded-full flex items-center justify-center bg-slate-100/90 dark:bg-slate-800/90 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:text-[#003E83] dark:hover:text-blue-400 hover:bg-blue-50/70 dark:hover:bg-blue-950/40 hover:border-blue-200 dark:hover:border-blue-800/80 shadow-2xs transition-all duration-300 ease-out active:scale-95 cursor-pointer shrink-0 group"
          title="Settings & Profile"
        >
          <Settings :size="15" class="transition-transform duration-300 ease-out group-hover:rotate-45" />
        </button>

      </div>

    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { Sparkles, WifiOff, AlertTriangle, Settings, Plus } from 'lucide-vue-next';

const props = defineProps({
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

defineEmits(['new-chat', 'open-settings']);

const isKhmer = computed(() => props.language === 'km');
</script>
