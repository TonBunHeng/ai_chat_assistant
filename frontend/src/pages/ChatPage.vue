<template>
  <div class="flex flex-col h-screen bg-[#fbfbfb] dark:bg-[#18181b] text-zinc-900 dark:text-zinc-100 transition-colors duration-200 overflow-hidden font-sans">
    
    <!-- Top Header Navigation -->
    <Header
      :sidebar-open="isSidebarOpen"
      :language="language"
      :is-online="isOnline"
      :mode="currentMode"
      @toggle-sidebar="toggleSidebar"
      @toggle-language="toggleLanguage"
      @open-settings="isSettingsOpen = true"
      @new-chat="handleNewChat"
    />

    <!-- Main Container with Sidebar + Chat Area -->
    <div class="flex flex-1 overflow-hidden relative">
      
      <!-- Collapsible ChatGPT-style Sidebar -->
      <Sidebar
        :is-open="isSidebarOpen"
        :sessions="sessions"
        :current-session-id="currentSessionId"
        :language="language"
        :user-profile="userProfile"
        :is-mobile="isMobile"
        @toggle="toggleSidebar"
        @close="isSidebarOpen = false"
        @select-session="handleSelectSession"
        @new-chat="handleNewChat"
        @delete-session="handleDeleteSession"
        @rename-session="handleRenameSession"
        @open-settings="isSettingsOpen = true"
      />

      <!-- Conversation Viewport -->
      <main class="flex-1 flex flex-col h-full min-w-0 bg-[#fbfbfb] dark:bg-[#18181b] relative">
        
        <!-- Welcome Screen (when conversation is empty) -->
        <div
          v-if="messages.length === 0"
          class="flex-1 flex flex-col items-center justify-center px-4 max-w-3xl mx-auto w-full -mt-8 sm:-mt-12 animate-fade-in"
        >
          <!-- Hero Badge & Title -->
          <div class="text-center mb-6 max-w-xl">
            <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-xs font-semibold text-zinc-700 dark:text-zinc-300 mb-3 shadow-2xs">
              <span>🇰🇭</span>
              <span>{{ isKhmer ? 'ជំនួយការឆ្លាតវៃកម្ពុជា Super AI' : 'Cambodia Super AI Assistant' }}</span>
            </div>
            <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold tracking-tight text-zinc-900 dark:text-white leading-tight">
              {{ isKhmer ? 'តើខ្ញុំអាចជួយដោះស្រាយ ឬស្វែងយល់អ្វីជូនអ្នកនៅថ្ងៃនេះ?' : 'What can I help you explore or solve today?' }}
            </h1>
            <p class="text-xs sm:text-sm text-zinc-500 dark:text-zinc-400 mt-2 max-w-md mx-auto">
              {{ isKhmer ? 'ឆ្លើយតបសំណួរទូទៅ សរសេរកូដ គណិតវិទ្យា ការបកប្រែ និងឯកទេសពេញលេញអំពីកម្ពុជា' : 'General intelligence, programming, math, translation, and deep Cambodia expertise.' }}
            </p>
          </div>

          <!-- Centered Input Pill -->
          <div class="w-full max-w-2xl">
            <ChatInput
              @send-message="handleSendMessage"
              @stop-generating="handleStopGenerating"
              :is-loading="isLoading"
              :language="language"
              :is-centered="true"
            />
          </div>

          <!-- Quick Starter Prompts -->
          <div class="mt-6 w-full max-w-2xl px-1 animate-fade-in">
            <div class="flex items-center justify-between mb-2 px-1">
              <span class="text-[11px] font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles :size="12" class="text-amber-500" />
                <span>{{ isKhmer ? 'ប្រធានបទណែនាំ' : 'Suggested Topics' }}</span>
              </span>
              <button
                type="button"
                @click="refreshWelcomePrompts"
                class="inline-flex items-center gap-1.5 text-[11px] font-medium text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white px-2 py-0.5 rounded-full hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-all cursor-pointer group active:scale-95"
                :title="isKhmer ? 'ប្តូរសំណួរថ្មី' : 'Refresh topics'"
              >
                <RotateCcw
                  :size="11"
                  :class="['transition-transform duration-500', isRefreshingWelcome ? '-rotate-180 text-zinc-900 dark:text-white' : 'group-hover:-rotate-90']"
                />
                <span>{{ isKhmer ? 'ប្តូរសំណួរ' : 'Refresh' }}</span>
              </button>
            </div>

            <!-- Starter Prompt Cards Grid (2x2) -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                v-for="(card, cIdx) in currentWelcomePrompts"
                :key="cIdx"
                @click="handleSendMessage(card.prompt)"
                class="flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl bg-white dark:bg-[#212121] border border-zinc-200/90 dark:border-zinc-800 text-xs sm:text-[13px] text-zinc-700 dark:text-zinc-300 hover:border-zinc-400 dark:hover:border-zinc-600 hover:text-zinc-900 dark:hover:text-white shadow-2xs hover:shadow-xs transition-all duration-200 active:scale-95 cursor-pointer text-left group"
              >
                <div class="w-7 h-7 rounded-lg bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center shrink-0 text-zinc-600 dark:text-zinc-400 group-hover:bg-zinc-200 dark:group-hover:bg-zinc-700 transition-colors">
                  <component :is="card.icon" :size="14" class="group-hover:scale-110 transition-transform duration-200" />
                </div>
                <span class="line-clamp-1 font-medium">{{ card.title }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Active Conversation State -->
        <template v-else>
          <ChatWindow
            :messages="messages"
            :is-loading="isLoading"
            :error="error"
            :language="language"
            @send-message="handleSendMessage"
            @regenerate="handleRegenerate"
            @edit-message="handleEditMessage"
          />
          <ChatInput
            @send-message="handleSendMessage"
            @stop-generating="handleStopGenerating"
            :is-loading="isLoading"
            :language="language"
            :is-centered="false"
          />
        </template>
      </main>
    </div>

    <!-- Settings Modal -->
    <SettingsModal
      :is-open="isSettingsOpen"
      :language="language"
      :user-profile="userProfile"
      @close="isSettingsOpen = false"
      @update:language="language = $event"
      @update:user-profile="userProfile = $event"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, markRaw } from 'vue';
import {
  Sparkles, RotateCcw, Landmark, Utensils, Calendar,
  Coins, Sun, MapPin, Code, Calculator, Languages, Briefcase
} from 'lucide-vue-next';
import Header from '../components/layout/Header.vue';
import Sidebar from '../components/layout/Sidebar.vue';
import ChatWindow from '../components/chat/ChatWindow.vue';
import ChatInput from '../components/chat/ChatInput.vue';
import SettingsModal from '../components/modals/SettingsModal.vue';
import { useOnlineStatus } from '../composables/useOnlineStatus';
import { performOfflineSearch } from '../utils/offlineSearch';
import {
  sendMessage,
  streamMessage,
  fetchChatSessions,
  fetchChatSession,
  renameChatSession,
  deleteChatSession,
  clearAllChatSessions,
} from '../services/chatService';

const { isOnline } = useOnlineStatus();
const language = ref('en');
const sessions = ref([]);
const currentSessionId = ref(null);
const messages = ref([]);
const isLoading = ref(false);
const error = ref(null);
const currentMode = ref('online');
const isSettingsOpen = ref(false);
const isSidebarOpen = ref(true);
const isMobile = ref(false);
const streamAbortController = ref(null);

const isKhmer = computed(() => language.value === 'km');

const checkMobileScreen = () => {
  const mobile = window.innerWidth < 768;
  isMobile.value = mobile;
  if (mobile && isSidebarOpen.value) {
    isSidebarOpen.value = false;
  }
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const toggleLanguage = () => {
  language.value = language.value === 'en' ? 'km' : 'en';
};

const enWelcomePromptsPool = [
  { id: 'code', icon: markRaw(Code), title: 'Write Python FastAPI service with auth', prompt: 'Write a clean, production-ready Python FastAPI web service with authentication and database models.' },
  { id: 'provinces', icon: markRaw(MapPin), title: 'Cambodia 25 Administrative Divisions', prompt: 'Give an overview of the 25 administrative divisions of Cambodia (24 provinces and Phnom Penh) with their unique specialties.' },
  { id: 'math', icon: markRaw(Calculator), title: 'Explain Gradient Descent step-by-step', prompt: 'Explain the mathematical foundation of Gradient Descent and show how to compute the derivative step by step.' },
  { id: 'temples', icon: markRaw(Landmark), title: 'Khmer Empire & Angkor Wat heritage', prompt: 'Tell me about the history of the Khmer Empire and the architectural marvels of Angkor Wat.' },
  { id: 'translate', icon: markRaw(Languages), title: 'Khmer to English natural translation', prompt: 'Translate this text into natural English: "សូមស្វាគមន៍មកកាន់ប្រទេសកម្ពុជា ទឹកដីនៃអរិយធម៌ដ៏រុងរឿង"' },
  { id: 'business', icon: markRaw(Briefcase), title: 'Starting a tech startup in Cambodia', prompt: 'What are the legal steps, opportunities, and digital payment ecosystems for launching a tech startup in Cambodia?' },
  { id: 'currency', icon: markRaw(Coins), title: 'Currency & USD vs Riel tips', prompt: 'What should I know about Cambodian currency, exchange rates, and tipping culture?' },
  { id: 'itinerary', icon: markRaw(Calendar), title: '3-Day Siem Reap cultural itinerary', prompt: 'Create a 3-day Siem Reap cultural itinerary' }
];

const kmWelcomePromptsPool = [
  { id: 'code', icon: markRaw(Code), title: 'សរសេរកូដ Python និង Web API', prompt: 'ជួយពន្យល់ និងសរសេរកូដ Python FastAPI សម្រាប់បង្កើត REST API ដោយមាន database និង authentication។' },
  { id: 'provinces', icon: markRaw(MapPin), title: 'រាជធានី-ខេត្តទាំង ២៥ នៃកម្ពុជា', prompt: 'សូមរៀបរាប់សង្ខេបអំពីរាជធានី-ខេត្តទាំង ២៥ នៅកម្ពុជា រួមទាំងសក្តានុពលសេដ្ឋកិច្ច និងទេសចរណ៍។' },
  { id: 'math', icon: markRaw(Calculator), title: 'គណិតវិទ្យា និង Algorithm', prompt: 'ជួយពន្យល់ពីគោលការណ៍ក្បួនដោះស្រាយ (Algorithm) និងភាពស្មុគស្មាញ Big-O notation។' },
  { id: 'temples', icon: markRaw(Landmark), title: 'ប្រវត្តិសាស្ត្រអង្គរ និងវប្បធម៌ខ្មែរ', prompt: 'សូមរៀបរាប់អំពីប្រវត្តិសាស្ត្រសម័យអង្គរដ៏រុងរឿង និងស្នាព្រះហស្តព្រះបាទជ័យវរ្ម័នទី ៧។' },
  { id: 'translate', icon: markRaw(Languages), title: 'បកប្រែភាសាអង់គ្លេស-ខ្មែរ ត្រឹមត្រូវតាមក្បួន', prompt: 'ជួយបកប្រែអត្ថបទនេះទៅជាភាសាខ្មែរផ្លូវការ៖ "Artificial intelligence empowers modern digital economies and innovation."' },
  { id: 'business', icon: markRaw(Briefcase), title: 'ការបង្កើតអាជីវកម្ម និងប្រព័ន្ធទូទាត់បាគង', prompt: 'តើការចុះបញ្ជីអាជីវកម្ម និងការរួមបញ្ចូលប្រព័ន្ធទូទាត់បាគង (Bakong KHQR) នៅកម្ពុជាមានជំហានអ្វីខ្លះ?' },
  { id: 'currency', icon: markRaw(Coins), title: 'ការចាយលុយដុល្លារ និងប្រាក់រៀល', prompt: 'តើការចាយលុយដុល្លារ និងប្រាក់រៀលនៅកម្ពុជាត្រូវដឹងអ្វីខ្លះ?' },
  { id: 'itinerary', icon: markRaw(Calendar), title: 'គម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប', prompt: 'រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប' }
];

const currentWelcomePrompts = ref([]);
const isRefreshingWelcome = ref(false);

const getFreshWelcomePrompts = (excludeIds = []) => {
  const pool = isKhmer.value ? kmWelcomePromptsPool : enWelcomePromptsPool;
  const available = pool.filter(p => !excludeIds.includes(p.id));
  const candidatePool = available.length >= 4 ? available : pool;
  const shuffled = [...candidatePool].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, 4);
};

const refreshWelcomePrompts = () => {
  isRefreshingWelcome.value = true;
  const currentIds = currentWelcomePrompts.value.map(p => p.id);
  currentWelcomePrompts.value = getFreshWelcomePrompts(currentIds);
  setTimeout(() => {
    isRefreshingWelcome.value = false;
  }, 400);
};

watch(
  () => language.value,
  () => {
    currentWelcomePrompts.value = getFreshWelcomePrompts();
  },
  { immediate: true }
);

// User Profile state with localStorage persistence
const getInitialProfile = () => {
  try {
    const stored = localStorage.getItem('cambodia_ai_user_profile');
    return stored ? JSON.parse(stored) : { name: 'Super AI User', email: '', travelStyle: 'cultural', preferredDestinations: ['siem_reap'] };
  } catch (e) {
    return { name: 'Super AI User', email: '', travelStyle: 'cultural', preferredDestinations: ['siem_reap'] };
  }
};

const userProfile = ref(getInitialProfile());

watch(userProfile, (newVal) => {
  try {
    localStorage.setItem('cambodia_ai_user_profile', JSON.stringify(newVal));
  } catch (e) {}
}, { deep: true });

watch(language, (newLang) => {
  try {
    document.documentElement.lang = newLang;
    document.documentElement.setAttribute('data-lang', newLang);
  } catch (e) {}
}, { immediate: true });

watch(isOnline, (online) => {
  currentMode.value = online ? 'online' : 'offline';
}, { immediate: true });

const ONE_HOUR_MS = 60 * 60 * 1000;

const loadLocalSessions = () => {
  try {
    const stored = localStorage.getItem('aichat_local_sessions');
    if (stored) {
      const parsed = JSON.parse(stored);
      if (Array.isArray(parsed)) {
        const now = Date.now();
        const validSessions = parsed.filter((s) => {
          const time = new Date(s.updated_at || s.created_at || now).getTime();
          return (now - time) < ONE_HOUR_MS;
        });

        if (validSessions.length !== parsed.length) {
          localStorage.setItem('aichat_local_sessions', JSON.stringify(validSessions));
        }

        sessions.value = validSessions;
        return validSessions;
      }
    }
  } catch (e) {
    console.error('Error reading local sessions from localStorage:', e);
  }
  return [];
};

const saveLocalSession = (newSession) => {
  try {
    const stored = localStorage.getItem('aichat_local_sessions');
    let localSessions = stored ? JSON.parse(stored) : [];
    if (!Array.isArray(localSessions)) localSessions = [];
    const idx = localSessions.findIndex((s) => s.session_id === newSession.session_id);
    if (idx >= 0) {
      localSessions[idx] = { ...localSessions[idx], ...newSession };
    } else {
      localSessions.unshift(newSession);
    }
    localStorage.setItem('aichat_local_sessions', JSON.stringify(localSessions));
    sessions.value = localSessions;
  } catch (e) {
    console.error('Error saving local session:', e);
  }
};

const loadSessions = async () => {
  try {
    const data = await fetchChatSessions();
    const sessionList = data || [];
    sessions.value = sessionList;
    return sessionList;
  } catch (err) {
    console.warn('Could not fetch online sessions. Falling back to local sessions storage:', err);
    return loadLocalSessions();
  }
};

const handleSelectSession = async (sessionId) => {
  if (!sessionId) return;
  currentSessionId.value = sessionId;
  localStorage.setItem('aichat_last_active_session_id', sessionId);
  error.value = null;

  if (isOnline.value) {
    try {
      const data = await fetchChatSession(sessionId);
      const resData = (data && data.data) ? data.data : data;
      if (resData && resData.messages && Array.isArray(resData.messages) && resData.messages.length > 0) {
        messages.value = resData.messages.map((m, idx) => ({
          id: m.id || (idx + 1),
          sender: m.sender || (m.role === 'assistant' ? 'ai' : m.role || 'user'),
          message: m.message || m.content || '',
          mode: m.mode || 'online',
          created_at: m.created_at || new Date().toISOString(),
        }));
        if (resData.metadata && resData.metadata.language) {
          language.value = resData.metadata.language;
        }
        return;
      }
    } catch (err) {
      console.warn('Online session fetch failed, checking local sessions:', err);
    }
  }

  try {
    const stored = localStorage.getItem('aichat_local_sessions');
    const localList = stored ? JSON.parse(stored) : [];
    const local = Array.isArray(localList) ? localList.find((s) => s.session_id === sessionId) : null;
    if (local && local.messages && Array.isArray(local.messages)) {
      messages.value = local.messages.map((m, idx) => ({
        id: m.id || (idx + 1),
        sender: m.sender || (m.role === 'assistant' ? 'ai' : m.role || 'user'),
        message: m.message || m.content || '',
        mode: m.mode || 'offline',
        created_at: m.created_at || new Date().toISOString(),
      }));
      if (local.language) {
        language.value = local.language;
      }
    }
  } catch (e) {
    console.error('Error reading local session backup:', e);
  }
};

const handleNewChat = () => {
  if (streamAbortController.value) {
    streamAbortController.value.abort();
    streamAbortController.value = null;
  }
  currentSessionId.value = null;
  localStorage.removeItem('aichat_last_active_session_id');
  messages.value = [];
  error.value = null;
  isLoading.value = false;
};

const handleClearChat = async () => {
  try {
    localStorage.removeItem('aichat_local_sessions');
    localStorage.removeItem('aichat_last_active_session_id');
  } catch (e) {
    console.error('Error clearing local session storage:', e);
  }
  sessions.value = [];
  handleNewChat();

  if (isOnline.value) {
    try {
      await clearAllChatSessions();
    } catch (err) {
      console.warn('Error clearing sessions on server:', err);
    }
  }
};

const handleDeleteSession = async (sessionId) => {
  if (!sessionId) return;

  try {
    const stored = localStorage.getItem('aichat_local_sessions');
    if (stored) {
      let localSessions = JSON.parse(stored);
      if (Array.isArray(localSessions)) {
        localSessions = localSessions.filter((s) => s.session_id !== sessionId);
        localStorage.setItem('aichat_local_sessions', JSON.stringify(localSessions));
      }
    }
  } catch (e) {
    console.error('Error updating local sessions:', e);
  }

  sessions.value = sessions.value.filter((s) => s.session_id !== sessionId);

  if (currentSessionId.value === sessionId) {
    handleNewChat();
  }

  if (isOnline.value) {
    try {
      await deleteChatSession(sessionId);
    } catch (err) {
      console.warn('Error deleting session on server:', err);
    }
  }
};

const handleRenameSession = async ({ sessionId, newTitle }) => {
  if (!sessionId || !newTitle) return;

  // 1. Update in local reactive state
  const target = sessions.value.find((s) => s.session_id === sessionId);
  if (target) {
    target.title = newTitle;
  }

  // 2. Update in localStorage
  try {
    const stored = localStorage.getItem('aichat_local_sessions');
    if (stored) {
      let localSessions = JSON.parse(stored);
      if (Array.isArray(localSessions)) {
        const idx = localSessions.findIndex((s) => s.session_id === sessionId);
        if (idx >= 0) {
          localSessions[idx].title = newTitle;
          localStorage.setItem('aichat_local_sessions', JSON.stringify(localSessions));
        }
      }
    }
  } catch (e) {
    console.error('Error renaming in localStorage:', e);
  }

  // 3. Update on server if online
  if (isOnline.value) {
    try {
      await renameChatSession(sessionId, newTitle);
    } catch (err) {
      console.warn('Error renaming session on server:', err);
    }
  }
};

const handleStopGenerating = () => {
  if (streamAbortController.value) {
    streamAbortController.value.abort();
    streamAbortController.value = null;
  }
  isLoading.value = false;
};

const handleSendMessage = async (text, attachments = [], isRegenerate = false) => {
  if (!text || !text.trim() || isLoading.value) return;

  error.value = null;
  const userMessageText = text.trim();

  // Optimistically append user message to UI if not regenerating
  if (!isRegenerate) {
    const tempUserMsg = {
      id: Date.now(),
      sender: 'user',
      message: userMessageText,
      attachments: attachments,
      created_at: new Date().toISOString(),
    };
    messages.value = [...messages.value, tempUserMsg];
  }
  isLoading.value = true;

  let activeSid = currentSessionId.value || `session_${Date.now()}`;
  currentSessionId.value = activeSid;
  localStorage.setItem('aichat_last_active_session_id', activeSid);

  const historyPayload = messages.value
    .filter((m) => m && (m.message || m.content))
    .map((m) => ({
      role: m.sender === 'user' || m.role === 'user' ? 'user' : 'assistant',
      content: m.message || m.content || '',
    }))
    .slice(-10);

  // Setup AI message placeholder in chat window
  const aiMsgId = Date.now() + 1;
  const aiMsg = {
    id: aiMsgId,
    sender: 'ai',
    message: '',
    mode: isOnline.value ? 'online' : 'offline',
    sources: [],
    suggestions: [],
    created_at: new Date().toISOString(),
  };
  messages.value = [...messages.value, aiMsg];

  let streamSucceeded = false;

  // 1. Try real-time SSE streaming when online
  if (isOnline.value) {
    streamAbortController.value = new AbortController();
    let accumulated = '';

    try {
      await streamMessage(
        {
          message: userMessageText,
          language: language.value,
          session_id: activeSid,
          history: historyPayload,
          attachments: attachments,
        },
        {
          signal: streamAbortController.value.signal,
          onChunk: (token) => {
            accumulated += token;
            const target = messages.value.find((m) => m.id === aiMsgId);
            if (target) {
              target.message = accumulated;
            }
          },
          onDone: () => {
            streamSucceeded = true;
          },
          onError: (err) => {
            console.warn('Streaming encountered an issue, will fallback to non-streaming API:', err);
          },
        }
      );
    } catch (streamErr) {
      console.warn('Streaming exception:', streamErr);
    } finally {
      streamAbortController.value = null;
    }
  }

  // 2. If streaming completed successfully and provided content
  const currentAiMsg = messages.value.find((m) => m.id === aiMsgId);
  if (streamSucceeded && currentAiMsg && currentAiMsg.message.trim().length > 0) {
    isLoading.value = false;
    currentMode.value = 'online';

    const firstUser = messages.value.find((m) => m.sender === 'user' || m.role === 'user');
    const title = firstUser ? firstUser.message : userMessageText;
    saveLocalSession({
      session_id: activeSid,
      title: title.slice(0, 50),
      language: language.value,
      created_at: new Date().toISOString(),
      messages: [...messages.value],
    });
    if (isOnline.value) loadSessions();
    return;
  }

  // 3. Fallback: Standard API call if streaming failed or produced no tokens
  try {
    if (isOnline.value) {
      try {
        const response = await sendMessage({
          message: userMessageText,
          language: language.value,
          session_id: activeSid,
          history: historyPayload,
          attachments: attachments,
        });

        const resData = response?.data;
        const apiPayload = (resData && typeof resData === 'object') ? resData : response;
        const answerText =
          apiPayload?.answer ||
          apiPayload?.message_text ||
          (apiPayload?.message && apiPayload.message !== 'Message processed successfully.' ? apiPayload.message : '') ||
          '';

        if (answerText) {
          if (currentAiMsg) {
            currentAiMsg.message = answerText;
            currentAiMsg.mode = apiPayload?.mode || 'online';
            currentAiMsg.model = apiPayload?.model;
            currentAiMsg.sources = apiPayload?.sources || [];
            currentAiMsg.suggestions = apiPayload?.suggestions || [];
            currentAiMsg.weather = apiPayload?.weather;
            currentAiMsg.currency = apiPayload?.currency;
            currentAiMsg.itinerary = apiPayload?.itinerary;
            currentAiMsg.recommendations = apiPayload?.recommendations;
          }
          currentMode.value = apiPayload?.mode || 'online';
          const firstUser = messages.value.find((m) => m.sender === 'user' || m.role === 'user');
          saveLocalSession({
            session_id: activeSid,
            title: (firstUser?.message || userMessageText).slice(0, 50),
            language: language.value,
            created_at: new Date().toISOString(),
            messages: [...messages.value],
          });
          loadSessions();
          isLoading.value = false;
          return;
        }
      } catch (apiErr) {
        console.warn('Standard API call failed, falling back to client-side offline search:', apiErr);
      }
    }

    // 4. Client-side Offline Search Fallback
    const offlineRes = await performOfflineSearch(userMessageText, language.value);
    if (currentAiMsg) {
      currentAiMsg.message = offlineRes.message || 'Cambodia Super AI is ready to help answer questions and explore Cambodia.';
      currentAiMsg.mode = 'offline';
      currentAiMsg.sources = offlineRes.sources || [];
      currentAiMsg.suggestions = offlineRes.suggestions || [];
    }
    currentMode.value = 'offline';

    const firstUser = messages.value.find((m) => m.sender === 'user' || m.role === 'user');
    saveLocalSession({
      session_id: activeSid,
      title: (firstUser?.message || userMessageText).slice(0, 50),
      language: language.value,
      created_at: new Date().toISOString(),
      messages: [...messages.value],
    });
  } catch (e) {
    console.error('Error in chat handler:', e);
    error.value = 'Failed to process message.';
  } finally {
    isLoading.value = false;
  }
};

const handleRegenerate = async () => {
  if (messages.value.length === 0 || isLoading.value) return;
  if (messages.value[messages.value.length - 1]?.sender === 'ai') {
    messages.value = messages.value.slice(0, -1);
  }
  const lastUserMsg = [...messages.value].reverse().find((m) => m.sender === 'user' || m.role === 'user');
  if (lastUserMsg && lastUserMsg.message) {
    handleSendMessage(lastUserMsg.message, lastUserMsg.attachments || [], true);
  }
};

const handleEditMessage = async ({ id, newText, index, message: origMsg }) => {
  if (!newText || !newText.trim() || isLoading.value) return;

  let targetIndex = index;
  if (targetIndex === undefined || targetIndex < 0) {
    targetIndex = messages.value.findIndex((m) => m.id === id);
  }
  if (targetIndex === -1) return;

  const attachments = origMsg?.attachments || messages.value[targetIndex]?.attachments || [];
  messages.value = messages.value.slice(0, targetIndex);
  await handleSendMessage(newText.trim(), attachments, false);
};

onMounted(() => {
  checkMobileScreen();
  window.addEventListener('resize', checkMobileScreen);

  loadLocalSessions();
  const lastSessionId = localStorage.getItem('aichat_last_active_session_id');
  if (lastSessionId) {
    handleSelectSession(lastSessionId);
  }

  if (isOnline.value) {
    loadSessions();
  }
});

onUnmounted(() => {
  window.removeEventListener('resize', checkMobileScreen);
  if (streamAbortController.value) {
    streamAbortController.value.abort();
  }
});
</script>
