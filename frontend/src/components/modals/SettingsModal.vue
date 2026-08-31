<template>
  <Transition name="modal">
    <div
      v-if="isOpen"
      @click="onClose"
      class="modal-backdrop fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/60 backdrop-blur-xs"
    >
      <div
        @click.stop
        class="modal-card bg-[#ffffff] dark:bg-[#18181b] rounded-2xl shadow-2xl border border-slate-200/80 dark:border-[#27272a] w-full max-w-[680px] h-[520px] max-h-[88vh] flex flex-col sm:flex-row overflow-hidden"
      >
        
        <!-- Left Sidebar -->
        <div class="sm:w-[210px] bg-slate-50/60 dark:bg-[#141416] p-3 sm:p-3.5 border-b sm:border-b-0 sm:border-r border-slate-100 dark:border-[#27272a] flex flex-col shrink-0">
          
          <!-- Top Left Close Button & Header -->
          <div class="flex items-center justify-between mb-3">
            <button
              @click="onClose"
              class="p-1.5 rounded-lg text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-200/70 dark:hover:bg-[#27272a] transition-colors cursor-pointer"
              title="Close"
            >
              <X :size="18" />
            </button>
            <span class="sm:hidden font-semibold text-xs text-slate-800 dark:text-slate-200">
              {{ isKhmer ? 'ការកំណត់' : 'Settings' }}
            </span>
          </div>

          <!-- Search Input Box -->
          <div class="relative mb-2.5">
            <Search :size="14" class="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              v-model="searchQuery"
              :placeholder="isKhmer ? 'ស្វែងរក...' : 'Search settings'"
              class="w-full pl-8 pr-2.5 py-1.5 bg-white dark:bg-[#1f1f23] border border-slate-200 dark:border-[#27272a] rounded-lg text-xs text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-slate-400 dark:focus:ring-slate-600 transition-all"
            />
          </div>

          <!-- Tab Navigation List -->
          <div class="flex sm:flex-col overflow-x-auto sm:overflow-x-visible gap-1 flex-1 scrollbar-none">
            <button
              v-for="tab in filteredTabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'flex items-center space-x-2.5 px-3 py-2 rounded-lg text-xs font-medium transition-all text-left cursor-pointer shrink-0 sm:w-full',
                activeTab === tab.id
                  ? 'bg-slate-200/80 dark:bg-[#27272a] text-slate-900 dark:text-white font-semibold'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#1f1f23]'
              ]"
            >
              <span :class="activeTab === tab.id ? 'text-slate-900 dark:text-white' : 'text-slate-400 dark:text-slate-500'">
                <component :is="tab.icon" :size="17" />
              </span>
              <span class="truncate">{{ isKhmer ? tab.labelKm : tab.labelEn }}</span>
            </button>
          </div>
        </div>

        <!-- Right Content Area -->
        <div class="flex-1 overflow-y-auto px-5 sm:px-6 py-4 sm:py-5 flex flex-col bg-white dark:bg-[#18181b]">
          
          <!-- Active Tab Title Header -->
          <div class="pb-3 mb-1 border-b border-slate-100 dark:border-[#27272a]">
            <h2 class="text-base sm:text-lg font-bold text-slate-900 dark:text-white">
              <template v-if="activeTab === 'general'">{{ isKhmer ? 'ទូទៅ (General)' : 'General' }}</template>
              <template v-else-if="activeTab === 'profile'">{{ isKhmer ? 'គណនី (Account)' : 'Account' }}</template>
              <template v-else-if="activeTab === 'travel'">{{ isKhmer ? 'ចំណូលចិត្តផ្ទាល់ខ្លួន (Personalization)' : 'Personalization' }}</template>
              <template v-else-if="activeTab === 'about'">{{ isKhmer ? 'អំពីប្រព័ន្ធ (About)' : 'About' }}</template>
            </h2>
          </div>

          <!-- Tab 1: General -->
          <div v-if="activeTab === 'general'" class="flex-1 divide-y divide-slate-100 dark:divide-[#27272a]">
            
            <!-- Appearance / Theme -->
            <div class="py-3.5 flex items-center justify-between">
              <div>
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  {{ isKhmer ? 'ស្បែកចំណុចប្រទាក់' : 'Appearance' }}
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  {{ isKhmer ? 'ជ្រើសរើសស្បែកពណ៌' : 'Choose color theme' }}
                </div>
              </div>

              <div class="flex items-center bg-slate-100 dark:bg-[#27272a] p-0.5 rounded-lg border border-slate-200 dark:border-[#333338]">
                <button
                  @click="toggleThemeIfDark"
                  :class="[
                    'flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs transition-all cursor-pointer',
                    !isDarkMode
                      ? 'bg-white dark:bg-[#18181b] text-slate-900 dark:text-white font-semibold shadow-2xs'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                  ]"
                >
                  <Sun :size="13" class="text-amber-500" />
                  <span>Light</span>
                </button>
                <button
                  @click="toggleThemeIfLight"
                  :class="[
                    'flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs transition-all cursor-pointer',
                    isDarkMode
                      ? 'bg-white dark:bg-[#18181b] text-slate-900 dark:text-white font-semibold shadow-2xs'
                      : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                  ]"
                >
                  <Moon :size="13" class="text-indigo-400" />
                  <span>Dark</span>
                </button>
              </div>
            </div>

            <!-- Language -->
            <div class="py-3.5 flex items-center justify-between">
              <div>
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  {{ isKhmer ? 'ភាសា' : 'Language' }}
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  {{ isKhmer ? 'ភាសាឆ្លើយតបចម្បង' : 'Primary conversation language' }}
                </div>
              </div>

              <div class="relative">
                <select
                  :value="language"
                  @change="$emit('update:language', $event.target.value)"
                  class="appearance-none bg-slate-100 dark:bg-[#27272a] border border-slate-200 dark:border-[#333338] text-slate-900 dark:text-white text-xs font-medium rounded-lg px-3 py-1.5 pr-7 focus:outline-none cursor-pointer"
                >
                  <option value="en">English (US)</option>
                  <option value="km">ភាសាខ្មែរ (Khmer)</option>
                </select>
                <ChevronDown :size="13" class="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
              </div>
            </div>

            <!-- Offline Data Cache -->
            <div class="py-3.5 flex items-center justify-between">
              <div>
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  {{ isKhmer ? 'ទិន្នន័យក្រៅបណ្តាញ' : 'Offline RAG Knowledge' }}
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  {{ isKhmer ? 'ស្វែងរកទិន្នន័យទេសចរណ៍ទោះគ្មានអ៊ីនធឺណិត' : 'Search local tourism data even without network' }}
                </div>
              </div>

              <span class="inline-flex items-center px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800 text-[11px] font-medium">
                Active
              </span>
            </div>

            <!-- Knowledge Source -->
            <div class="py-3.5 flex items-center justify-between">
              <div>
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  {{ isKhmer ? 'ប្រភពទិន្នន័យ' : 'Knowledge Source' }}
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  {{ isKhmer ? 'ផ្អែកលើទិន្នន័យទេសចរណ៍ផ្លូវការកម្ពុជា' : 'Cambodia Tourism Official Database' }}
                </div>
              </div>

              <ShieldCheck :size="18" class="text-blue-500" />
            </div>
          </div>

          <!-- Tab 2: Profile -->
          <div v-if="activeTab === 'profile'" class="flex-1 divide-y divide-slate-100 dark:divide-[#27272a]">
            <!-- Display Name -->
            <div class="py-3.5 flex items-center justify-between gap-4">
              <div class="shrink-0">
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  {{ isKhmer ? 'ឈ្មោះអ្នកប្រើប្រាស់' : 'Display Name' }}
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  {{ isKhmer ? 'ឈ្មោះដែល AI ប្រើសម្រាប់ហៅអ្នក' : 'Name used in AI greetings' }}
                </div>
              </div>

              <input
                type="text"
                :value="userProfile.name || ''"
                @input="updateProfileField('name', $event.target.value)"
                placeholder="Traveler"
                class="w-44 sm:w-56 px-3 py-1.5 text-xs bg-slate-100 dark:bg-[#27272a] border border-slate-200 dark:border-[#333338] rounded-lg text-slate-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-slate-400"
              />
            </div>

            <!-- Email -->
            <div class="py-3.5 flex items-center justify-between gap-4">
              <div class="shrink-0">
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  {{ isKhmer ? 'អ៊ីមែល (មិនបាច់បំពេញ)' : 'Email' }}
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  {{ isKhmer ? 'សម្រាប់ទទួលព័ត៌មានធ្វើដំណើរ' : 'Optional contact' }}
                </div>
              </div>

              <input
                type="email"
                :value="userProfile.email || ''"
                @input="updateProfileField('email', $event.target.value)"
                placeholder="user@example.com"
                class="w-44 sm:w-56 px-3 py-1.5 text-xs bg-slate-100 dark:bg-[#27272a] border border-slate-200 dark:border-[#333338] rounded-lg text-slate-900 dark:text-white focus:outline-none focus:ring-1 focus:ring-slate-400"
              />
            </div>

            <!-- Data Privacy -->
            <div class="py-3.5 flex items-center justify-between">
              <div>
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  {{ isKhmer ? 'ការរក្សាទុកទិន្នន័យ' : 'Data Privacy' }}
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  {{ isKhmer ? 'រក្សាទុកក្នុងឧបករណ៍របស់អ្នកដោយសុវត្ថិភាព' : 'Stored securely in local browser storage' }}
                </div>
              </div>

              <Lock :size="16" class="text-slate-400" />
            </div>
          </div>

          <!-- Tab 3: Personalization -->
          <div v-if="activeTab === 'travel'" class="flex-1 divide-y divide-slate-100 dark:divide-[#27272a]">
            
            <!-- Travel Persona -->
            <div class="py-3.5 flex flex-col gap-2">
              <div class="flex items-center justify-between">
                <div>
                  <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                    {{ isKhmer ? 'ស្ទីលនៃការដើរលេង' : 'Travel Style' }}
                  </div>
                  <div class="text-[11px] text-slate-400 dark:text-slate-500">
                    {{ isKhmer ? 'ជ្រើសរើសស្ទីលដើម្បីឱ្យ AI ណែនាំត្រូវចំណូលចិត្ត' : 'Helps AI suggest tailored attractions & tips' }}
                  </div>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-2 mt-1">
                <button
                  v-for="style in travelStyles"
                  :key="style.id"
                  @click="updateProfileField('travelStyle', style.id)"
                  :class="[
                    'px-3 py-2 rounded-lg text-xs text-left transition-all border cursor-pointer',
                    userProfile.travelStyle === style.id
                      ? 'bg-slate-100 dark:bg-[#27272a] border-slate-400 dark:border-slate-500 font-semibold text-slate-900 dark:text-white'
                      : 'border-slate-200 dark:border-[#27272a] text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#1f1f23]'
                  ]"
                >
                  {{ isKhmer ? style.nameKm : style.nameEn }}
                </button>
              </div>
            </div>

            <!-- Favorite Destinations -->
            <div class="py-3.5 flex flex-col gap-2">
              <div>
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  {{ isKhmer ? 'ខេត្ត/ក្រុងដែលចូលចិត្ត' : 'Favorite Destinations' }}
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  {{ isKhmer ? 'ជ្រើសរើសខេត្ត/ក្រុងដែលចង់ទៅកម្សាន្ត' : 'Select top Cambodian destinations' }}
                </div>
              </div>

              <div class="flex flex-wrap gap-1.5 mt-1">
                <button
                  v-for="dest in destinations"
                  :key="dest.id"
                  @click="toggleDestination(dest.id)"
                  :class="[
                    'px-3 py-1.5 rounded-lg text-xs font-medium transition-all border cursor-pointer flex items-center space-x-1.5',
                    (userProfile.preferredDestinations || []).includes(dest.id)
                      ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 border-transparent shadow-2xs font-semibold'
                      : 'bg-slate-100 dark:bg-[#27272a] text-slate-700 dark:text-slate-300 border-slate-200 dark:border-[#333338] hover:bg-slate-200/70'
                  ]"
                >
                  <span>{{ isKhmer ? dest.nameKm : dest.nameEn }}</span>
                  <Check v-if="(userProfile.preferredDestinations || []).includes(dest.id)" :size="12" />
                </button>
              </div>
            </div>
          </div>

          <!-- Tab 4: About -->
          <div v-if="activeTab === 'about'" class="flex-1 divide-y divide-slate-100 dark:divide-[#27272a]">
            <!-- Application -->
            <div class="py-3.5 flex items-center justify-between">
              <div>
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  Application
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  AI Tourism Information Service (Cambodia)
                </div>
              </div>
              <div class="font-semibold text-xs text-slate-900 dark:text-white">
                Angkor Verse AI
              </div>
            </div>

            <!-- Version -->
            <div class="py-3.5 flex items-center justify-between">
              <div>
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  Version
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  Current system release
                </div>
              </div>
              <div class="text-xs text-slate-500 dark:text-slate-400 font-mono">
                v2.5.0
              </div>
            </div>

            <!-- Specialization -->
            <div class="py-3.5 flex items-center justify-between">
              <div>
                <div class="text-xs sm:text-sm font-medium text-slate-900 dark:text-white">
                  Specialization
                </div>
                <div class="text-[11px] text-slate-400 dark:text-slate-500">
                  World Heritage, Temples, Culture & Travel Plans
                </div>
              </div>
              <span class="text-xs font-medium text-slate-700 dark:text-slate-300">
                Cambodia
              </span>
            </div>
          </div>

        </div>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, markRaw } from 'vue';
import {
  X, Settings, Moon, Sun, User, Sparkles, Search, ChevronDown, Lock, ShieldCheck, Check, Info
} from 'lucide-vue-next';
import { useTheme } from '../../composables/useTheme';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  language: {
    type: String,
    default: 'en',
  },
  userProfile: {
    type: Object,
    default: () => ({
      name: 'Traveler',
      email: '',
      travelStyle: 'cultural',
      preferredDestinations: ['siem_reap'],
    }),
  },
});

const emit = defineEmits(['close', 'update:language', 'update:userProfile']);

const { isDarkMode, toggleTheme } = useTheme();
const activeTab = ref('general');
const searchQuery = ref('');

const isKhmer = computed(() => props.language === 'km');

const onClose = () => {
  emit('close');
};

const toggleThemeIfDark = () => {
  if (isDarkMode.value) toggleTheme();
};

const toggleThemeIfLight = () => {
  if (!isDarkMode.value) toggleTheme();
};

const destinations = [
  { id: 'siem_reap', nameEn: 'Siem Reap (Angkor)', nameKm: 'សៀមរាប (អង្គរ)' },
  { id: 'phnom_penh', nameEn: 'Phnom Penh', nameKm: 'ភ្នំពេញ' },
  { id: 'kampot', nameEn: 'Kampot & Kep', nameKm: 'កំពត និង កែប' },
  { id: 'islands', nameEn: 'Koh Rong & Islands', nameKm: 'កោះរ៉ុង និង កោះកែប' },
];

const travelStyles = [
  { id: 'cultural', nameEn: 'Cultural & Heritage', nameKm: 'វប្បធម៌ និង បេតិកភណ្ឌ' },
  { id: 'foodie', nameEn: 'Food & Culinary', nameKm: 'ម្ហូបអាហារ និង ភេសជ្ជៈ' },
  { id: 'adventure', nameEn: 'Nature & Adventure', nameKm: 'ធម្មជាតិ និង ផ្សងព្រេង' },
  { id: 'luxury', nameEn: 'Relaxation & Resorts', nameKm: 'លំហែកាយ និង សម្រាក' },
];

const tabs = [
  { id: 'general', labelEn: 'General', labelKm: 'ទូទៅ', icon: markRaw(Settings) },
  { id: 'profile', labelEn: 'Account', labelKm: 'គណនី', icon: markRaw(User) },
  { id: 'travel', labelEn: 'Personalization', labelKm: 'ចំណូលចិត្តផ្ទាល់ខ្លួន', icon: markRaw(Sparkles) },
  { id: 'about', labelEn: 'About', labelKm: 'អំពីប្រព័ន្ធ', icon: markRaw(Info) },
];

const filteredTabs = computed(() => {
  if (!searchQuery.value.trim()) return tabs;
  const q = searchQuery.value.toLowerCase();
  return tabs.filter(t => t.labelEn.toLowerCase().includes(q) || t.labelKm.includes(q));
});

const updateProfileField = (field, value) => {
  emit('update:userProfile', {
    ...props.userProfile,
    [field]: value,
  });
};

const toggleDestination = (id) => {
  const current = props.userProfile.preferredDestinations || [];
  const updated = current.includes(id)
    ? current.filter(item => item !== id)
    : [...current, id];
  updateProfileField('preferredDestinations', updated);
};

const handleKeyDown = (e) => {
  if (e.key === 'Escape' && props.isOpen) {
    onClose();
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<style scoped>
/* Vue Modal Transition for smooth 200ms fade + scale */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease-out;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-card,
.modal-leave-active .modal-card {
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease-out;
}

.modal-enter-from .modal-card {
  opacity: 0;
  transform: scale(0.95) translateY(8px);
}

.modal-leave-to .modal-card {
  opacity: 0;
  transform: scale(0.95) translateY(8px);
}
</style>
