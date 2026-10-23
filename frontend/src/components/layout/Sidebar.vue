<template>
  <!-- Sidebar Aside Container -->
  <aside
    :class="[
      'flex flex-col h-full bg-[#fbfbfb] dark:bg-[#18181b] border-zinc-200 dark:border-zinc-800/80 select-none shrink-0 transition-all duration-300 ease-in-out',
      // Mobile styles: fixed drawer overlay below 56px header
      'fixed top-14 bottom-0 left-0 z-40 w-[280px] max-w-[85vw] border-r shadow-2xl',
      isOpen ? 'translate-x-0' : '-translate-x-full pointer-events-none',
      // Desktop styles: in-flow collapsible sidebar beside main chat
      'md:relative md:top-0 md:bottom-auto md:left-auto md:z-10 md:max-w-none md:shadow-none md:pointer-events-auto md:translate-x-0',
      isOpen ? 'md:w-[280px] md:border-r' : 'md:w-0 md:border-r-0 md:overflow-hidden'
    ]"
  >
    <!-- Teleported mobile backdrop attached directly to body -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition-opacity duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isOpen && isMobile"
          @click="$emit('close')"
          class="fixed inset-x-0 top-14 bottom-0 z-30 bg-black/40 backdrop-blur-xs md:hidden cursor-pointer"
          aria-label="Close sidebar backdrop"
        />
      </Transition>
    </Teleport>

    <!-- Fixed-width inner column: prevents text wrapping or squashing while collapsing -->
    <div class="w-[280px] h-full flex flex-col min-h-0 overflow-hidden">
      
      <!-- Top Action Bar -->
      <div class="p-3 border-b border-zinc-200/80 dark:border-zinc-800/80 flex items-center justify-between gap-2 shrink-0">
        <button
          type="button"
          @click="handleNewChat"
          class="flex-1 flex items-center justify-between px-3 h-9 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 hover:border-zinc-300 dark:hover:border-zinc-700 text-zinc-800 dark:text-zinc-200 text-xs sm:text-[13px] font-semibold transition-all duration-150 shadow-2xs hover:shadow-xs active:scale-98 cursor-pointer group"
          :title="isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat'"
        >
          <div class="flex items-center space-x-2">
            <Plus :size="15" class="text-zinc-600 dark:text-zinc-400 group-hover:text-zinc-900 dark:group-hover:text-white" />
            <span>{{ isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat' }}</span>
          </div>
          <span class="text-[10px] text-zinc-400 font-mono hidden sm:inline">⌘N</span>
        </button>

        <!-- Collapse Sidebar Button -->
        <button
          type="button"
          @click="$emit('toggle')"
          class="w-9 h-9 flex items-center justify-center rounded-xl text-zinc-500 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors cursor-pointer shrink-0"
          :title="isKhmer ? 'បិទរបារចំហៀង' : 'Close Sidebar'"
        >
          <PanelLeftClose :size="16" />
        </button>
      </div>

      <!-- Search Conversations Input -->
      <div class="px-3 pt-3 pb-1 shrink-0">
        <div class="relative flex items-center">
          <Search :size="13" class="absolute left-2.5 text-zinc-400 pointer-events-none" />
          <input
            type="text"
            v-model="searchQuery"
            :placeholder="isKhmer ? 'ស្វែងរកកិច្ចសន្ទនា...' : 'Search chats...'"
            class="w-full h-8 pl-8 pr-7 rounded-lg bg-zinc-100/90 dark:bg-zinc-900 border border-transparent focus:border-zinc-300 dark:focus:border-zinc-700 focus:bg-white dark:focus:bg-black text-xs text-zinc-800 dark:text-zinc-200 placeholder-zinc-400 focus:outline-none transition-all"
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            type="button"
            class="absolute right-2 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 cursor-pointer"
          >
            <X :size="12" />
          </button>
        </div>
      </div>

      <!-- Cambodia Service Categories -->
      <div class="px-2 pt-1 pb-1 shrink-0 border-b border-zinc-200/60 dark:border-zinc-800/60">
        <button
          type="button"
          @click="showCategories = !showCategories"
          class="w-full flex items-center justify-between px-2 py-1.5 rounded-lg text-[11px] font-semibold text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800/60 transition-colors cursor-pointer"
        >
          <span class="flex items-center gap-1.5">
            <span>🇰🇭</span>
            <span>{{ isKhmer ? 'សេវាកម្មកម្ពុជា' : 'Cambodia Services' }}</span>
          </span>
          <ChevronDown :size="12" :class="['transition-transform duration-200', showCategories ? 'rotate-180' : '']" />
        </button>

        <div v-show="showCategories" class="mt-1 space-y-0.5 max-h-40 overflow-y-auto scrollbar-thin pb-1">
          <button
            v-for="cat in cambodiaCategories"
            :key="cat.id"
            @click="handleSelectCategory(cat)"
            type="button"
            class="w-full flex items-center space-x-2 px-2 py-1.5 rounded-lg text-xs text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800/80 transition-colors text-left cursor-pointer group"
          >
            <component :is="cat.icon" :size="13" class="shrink-0 text-zinc-400 group-hover:text-zinc-800 dark:group-hover:text-zinc-200 transition-colors" />
            <span class="truncate">{{ isKhmer ? cat.nameKm : cat.nameEn }}</span>
          </button>
        </div>
      </div>

      <!-- Conversation History List (Scrolls independently) -->
      <div class="flex-1 overflow-y-auto px-2 py-2 space-y-1 min-h-0 scrollbar-thin">
        <div v-if="filteredSessions.length === 0" class="py-8 text-center text-zinc-400 text-xs">
          <MessageSquare :size="20" class="mx-auto mb-2 opacity-40" />
          <span>{{ isKhmer ? 'មិនមានប្រវត្តិសន្ទនាទេ' : 'No chats found' }}</span>
        </div>

        <template v-else>
          <div
            v-for="sess in filteredSessions"
            :key="sess.session_id"
            :class="[
              'group relative flex items-center justify-between w-full h-9 px-2.5 rounded-lg text-xs font-medium transition-all duration-150 cursor-pointer',
              currentSessionId === sess.session_id
                ? 'bg-zinc-200/80 dark:bg-zinc-800 text-zinc-900 dark:text-white font-semibold'
                : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 hover:text-zinc-900 dark:hover:text-zinc-200'
            ]"
            @click="handleSelect(sess.session_id)"
          >
            <!-- Left: Icon & Title -->
            <div class="flex items-center space-x-2 min-w-0 flex-1 pr-1">
              <MessageSquare :size="13" class="shrink-0 opacity-70 group-hover:opacity-100" />

              <!-- Inline Renaming Mode -->
              <form
                v-if="editingSessionId === sess.session_id"
                @submit.prevent="saveRename(sess.session_id)"
                class="flex-1 flex items-center"
                @click.stop
              >
                <input
                  ref="renameInputRef"
                  type="text"
                  v-model="editTitle"
                  @keydown.esc="cancelRename"
                  class="w-full h-6 px-1.5 rounded bg-white dark:bg-zinc-900 border border-zinc-400 dark:border-zinc-600 text-xs text-zinc-900 dark:text-white focus:outline-none"
                  autofocus
                />
                <button
                  type="submit"
                  class="ml-1 text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 p-0.5"
                  title="Save"
                >
                  <Check :size="12" />
                </button>
                <button
                  type="button"
                  @click="cancelRename"
                  class="text-zinc-400 hover:text-zinc-600 p-0.5"
                  title="Cancel"
                >
                  <X :size="12" />
                </button>
              </form>

              <!-- Normal Title Display -->
              <span v-else class="truncate">
                {{ sess.title || (isKhmer ? 'កិច្ចសន្ទនាថ្មី' : 'New Chat') }}
              </span>
            </div>

            <!-- Right Action Buttons (on hover or active) -->
            <div
              v-if="editingSessionId !== sess.session_id"
              class="items-center space-x-0.5 hidden group-hover:flex"
              @click.stop
            >
              <!-- Rename Button -->
              <button
                type="button"
                @click="startRename(sess)"
                class="p-1 rounded text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors"
                :title="isKhmer ? 'ប្តូរឈ្មោះ' : 'Rename'"
              >
                <Pencil :size="11" />
              </button>

              <!-- Delete Button -->
              <button
                type="button"
                @click="$emit('delete-session', sess.session_id)"
                class="p-1 rounded text-zinc-400 hover:text-rose-600 dark:hover:text-rose-400 hover:bg-zinc-200 dark:hover:bg-zinc-700 transition-colors"
                :title="isKhmer ? 'លុបកិច្ចសន្ទនា' : 'Delete'"
              >
                <Trash2 :size="11" />
              </button>
            </div>
          </div>
        </template>
      </div>

      <!-- Bottom User Profile Section (Anchored to bottom) -->
      <div class="p-3 border-t border-zinc-200/80 dark:border-zinc-800/80 shrink-0 bg-white/50 dark:bg-zinc-900/40">
        <div class="flex items-center justify-between p-1.5 rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800/60 transition-colors">
          <div class="flex items-center space-x-2.5 min-w-0">
            <div class="w-8 h-8 rounded-full bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 flex items-center justify-center font-bold text-xs shrink-0 shadow-2xs">
              {{ userInitials }}
            </div>
            <div class="min-w-0">
              <span class="text-xs font-semibold text-zinc-900 dark:text-white block truncate">
                {{ displayName }}
              </span>
              <span class="text-[10px] text-zinc-400 dark:text-zinc-500 block -mt-0.5 truncate">
                Super AI Assistant
              </span>
            </div>
          </div>

          <!-- Settings Button -->
          <button
            type="button"
            @click="$emit('open-settings')"
            class="w-7 h-7 flex items-center justify-center rounded-lg text-zinc-500 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white hover:bg-zinc-200/70 dark:hover:bg-zinc-700/60 transition-colors cursor-pointer shrink-0"
            :title="isKhmer ? 'ការកំណត់' : 'Settings'"
          >
            <Settings :size="14" />
          </button>
        </div>
      </div>

    </div>
  </aside>
</template>

<script setup>
import { ref, computed, nextTick, markRaw } from 'vue';
import {
  Plus, Search, MessageSquare, Pencil, Trash2, Check, X,
  Settings, PanelLeftClose, ChevronDown, Landmark, Languages,
  Briefcase, GraduationCap, Building2, Cpu
} from 'lucide-vue-next';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: true,
  },
  sessions: {
    type: Array,
    default: () => [],
  },
  currentSessionId: {
    type: String,
    default: null,
  },
  language: {
    type: String,
    default: 'en',
  },
  userProfile: {
    type: Object,
    default: () => ({ name: 'Traveler' }),
  },
  isMobile: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits([
  'toggle',
  'close',
  'select-session',
  'new-chat',
  'delete-session',
  'rename-session',
  'open-settings',
  'select-category',
]);

const showCategories = ref(true);

const cambodiaCategories = [
  {
    id: 'tourism',
    icon: markRaw(Landmark),
    nameEn: 'Tourism & Travel',
    nameKm: 'ទេសចរណ៍ & ដំណើរកម្សាន្ត',
    promptEn: 'Plan a 3-day trip to Siem Reap with travel recommendations and itinerary.',
    promptKm: 'សូមរៀបចំគម្រោងដំណើរកម្សាន្ត ៣ ថ្ងៃនៅសៀមរាប ជាមួយការណែនាំទីកន្លែង និងកញ្ចប់ថវិកា។'
  },
  {
    id: 'language',
    icon: markRaw(Languages),
    nameEn: 'Khmer Language',
    nameKm: 'ភាសាខ្មែរ & ការបកប្រែ',
    promptEn: 'Translate Khmer to English and explain formal writing nuance: "សូមគោរពជម្រាបសួរលោកប្រធាន"',
    promptKm: 'ជួយណែនាំទម្រង់លិខិតរដ្ឋបាលផ្លូវការជាភាសាខ្មែរ តាមក្បួនអក្ខរាវិរុទ្ធវចនានុក្រមសម្ដេចសង្ឃរាជ ជួន ណាត។'
  },
  {
    id: 'business',
    icon: markRaw(Briefcase),
    nameEn: 'Business & Economy',
    nameKm: 'ធុរកិច្ច & សេដ្ឋកិច្ច',
    promptEn: 'Explain Cambodian business registration procedures via CamDX and tax obligations.',
    promptKm: 'ពន្យល់ពីនីតិវិធីនៃការចុះបញ្ជីអាជីវកម្មតាម CamDX និងកាតព្វកិច្ចពន្ធដារនៅកម្ពុជា។'
  },
  {
    id: 'education',
    icon: markRaw(GraduationCap),
    nameEn: 'Education & Research',
    nameKm: 'ការអប់រំ & ការស្រាវជ្រាវ',
    promptEn: 'Provide a Grade 12 BacII study guide for mathematics and Cambodian science curriculum.',
    promptKm: 'ជួយណែនាំវិធីសាស្ត្ររៀបចំប្រឡងសញ្ញាបត្រមធ្យមសិក្សាទុតិយភូមិ (បាក់ឌុប) ថ្នាក់ទី ១២ និងមុខវិជ្ជាស្នូល។'
  },
  {
    id: 'government',
    icon: markRaw(Building2),
    nameEn: 'Public Services',
    nameKm: 'រដ្ឋបាល & សេវាសាធារណៈ',
    promptEn: 'Find official Cambodian government information regarding passport issuance and e-Visa.',
    promptKm: 'ស្វែងរកព័ត៌មានផ្លូវការអំពីការធ្វើលិខិតឆ្លងដែនខ្មែរ (GDI) និងទិដ្ឋាការអេឡិចត្រូនិក e-Visa។'
  },
  {
    id: 'technology',
    icon: markRaw(Cpu),
    nameEn: 'Technology & AI',
    nameKm: 'បច្ចេកវិទ្យា & AI',
    promptEn: 'Build an AI application with Laravel, Vue.js, and Bakong KHQR payment integration.',
    promptKm: 'របៀបបង្កើតកម្មវិធី AI ដោយប្រើ Laravel, Vue.js និងការតភ្ជាប់ជាមួយប្រព័ន្ធ Bakong KHQR Open API។'
  }
];

const handleSelectCategory = (cat) => {
  const prompt = isKhmer.value ? cat.promptKm : cat.promptEn;
  emit('select-category', prompt);
};

const searchQuery = ref('');
const editingSessionId = ref(null);
const editTitle = ref('');
const renameInputRef = ref(null);

const isKhmer = computed(() => props.language === 'km');

const displayName = computed(() => {
  return props.userProfile?.name?.trim() || 'Traveler';
});

const userInitials = computed(() => {
  return displayName.value.charAt(0).toUpperCase();
});

const filteredSessions = computed(() => {
  if (!props.sessions) return [];
  if (!searchQuery.value.trim()) return props.sessions;
  const q = searchQuery.value.toLowerCase().trim();
  return props.sessions.filter(
    (s) => s.title && s.title.toLowerCase().includes(q)
  );
});

const handleSelect = (sessionId) => {
  emit('select-session', sessionId);
  if (props.isMobile) {
    emit('close');
  }
};

const handleNewChat = () => {
  emit('new-chat');
  if (props.isMobile) {
    emit('close');
  }
};

const startRename = (sess) => {
  editingSessionId.value = sess.session_id;
  editTitle.value = sess.title || '';
  nextTick(() => {
    renameInputRef.value?.focus();
  });
};

const saveRename = (sessionId) => {
  if (editTitle.value.trim()) {
    emit('rename-session', { sessionId, newTitle: editTitle.value.trim() });
  }
  editingSessionId.value = null;
  editTitle.value = '';
};

const cancelRename = () => {
  editingSessionId.value = null;
  editTitle.value = '';
};
</script>
