<template>
  <div class="flex flex-col h-screen bg-[#f8fafc] dark:bg-[#18181b] text-slate-900 dark:text-slate-100 transition-colors duration-200 overflow-hidden font-sans">
    
    <!-- Header -->
    <Header
      :language="language"
      :is-online="isOnline"
      :mode="currentMode"
      @open-settings="isSettingsOpen = true"
      @new-chat="handleNewChat"
    />

    <!-- Main Container -->
    <div class="flex flex-1 overflow-hidden relative">
      <main class="flex-1 flex flex-col h-full min-w-0">
        
        <!-- Empty Welcome State -->
        <div
          v-if="messages.length === 0"
          class="flex-1 flex flex-col items-center justify-center px-3 sm:px-4 max-w-3xl mx-auto w-full -mt-10 sm:-mt-16 animate-fade-in"
        >
          <h1 class="text-xl sm:text-2xl md:text-3xl lg:text-[32px] font-bold tracking-tight text-slate-900 dark:text-white text-center sm:whitespace-nowrap mb-6 select-none px-2 max-w-full leading-snug">
            {{ isKhmer ? 'តើខ្ញុំអាចជួយអ្នកទស្សនាកម្ពុជាយ៉ាងដូចម្តេច?' : 'How can I help tourists visit Cambodia?' }}
          </h1>
          <div class="w-full max-w-2xl">
            <ChatInput
              @send-message="handleSendMessage"
              :is-loading="isLoading"
              :language="language"
              :is-centered="true"
            />
          </div>

          <!-- Quick Starter Prompts -->
          <div class="mt-6 w-full max-w-2xl px-1 animate-fade-in">
            <div class="flex items-center justify-between mb-2 px-1">
              <span class="text-[11px] font-semibold text-slate-400 dark:text-zinc-500 uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles :size="12" class="text-amber-500" />
                <span>{{ isKhmer ? 'សំណើណែនាំ' : 'Suggested Topics' }}</span>
              </span>
              <button
                type="button"
                @click="refreshWelcomePrompts"
                class="inline-flex items-center gap-1.5 text-[11px] font-medium text-slate-500 dark:text-zinc-400 hover:text-[#003E83] dark:hover:text-blue-400 px-2 py-0.5 rounded-full hover:bg-slate-100 dark:hover:bg-zinc-800 transition-all cursor-pointer group active:scale-95"
                :title="isKhmer ? 'ប្តូរសំណួរថ្មី' : 'Refresh questions'"
              >
                <RotateCcw
                  :size="11"
                  :class="['transition-transform duration-500', isRefreshingWelcome ? '-rotate-180 text-[#003E83] dark:text-blue-400' : 'group-hover:-rotate-90']"
                />
                <span>{{ isKhmer ? 'ប្តូរសំណួរ' : 'Refresh' }}</span>
              </button>
            </div>

            <!-- Starter Prompt Cards Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <button
                v-for="(card, cIdx) in currentWelcomePrompts"
                :key="cIdx"
                @click="handleSendMessage(card.prompt)"
                class="flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl bg-white dark:bg-[#212121] border border-slate-200/90 dark:border-zinc-800 text-xs sm:text-[13px] text-slate-700 dark:text-slate-300 hover:border-[#003E83] dark:hover:border-blue-500 hover:text-[#003E83] dark:hover:text-blue-400 shadow-2xs hover:shadow-xs transition-all duration-200 active:scale-95 cursor-pointer text-left group"
              >
                <div class="w-7 h-7 rounded-lg bg-slate-100 dark:bg-zinc-800 flex items-center justify-center shrink-0 text-[#003E83] dark:text-blue-400 group-hover:bg-blue-50 dark:group-hover:bg-blue-950/40 transition-colors">
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
import { ref, computed, watch, onMounted, markRaw } from 'vue';
import {
  Sparkles, RotateCcw, Landmark, Utensils, Calendar,
  Palmtree, Coins, Sun, Compass, MapPin
} from 'lucide-vue-next';
import Header from '../components/layout/Header.vue';
import ChatWindow from '../components/chat/ChatWindow.vue';
import ChatInput from '../components/chat/ChatInput.vue';
import SettingsModal from '../components/modals/SettingsModal.vue';
import { useOnlineStatus } from '../composables/useOnlineStatus';
import { performOfflineSearch } from '../utils/offlineSearch';
import {
  sendMessage,
  fetchChatSessions,
  fetchChatSession,
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

const isKhmer = computed(() => language.value === 'km');

const enWelcomePromptsPool = [
  { id: 'temples', icon: markRaw(Landmark), title: 'Must-see temples beyond Angkor', prompt: 'What must-see temples in Siem Reap should I visit besides Angkor Wat?' },
  { id: 'crab', icon: markRaw(Utensils), title: 'Fresh Kampot pepper crab in Kep', prompt: 'Tell me about fresh Kampot pepper crab in Kep' },
  { id: 'itinerary', icon: markRaw(Calendar), title: '3-Day Siem Reap cultural itinerary', prompt: 'Create a 3-day Siem Reap cultural itinerary' },
  { id: 'beach', icon: markRaw(Palmtree), title: 'Best white sand beaches on Koh Rong', prompt: 'What are the most beautiful beaches on Koh Rong island?' },
  { id: 'currency', icon: markRaw(Coins), title: 'Currency & USD vs Riel tips', prompt: 'What should I know about Cambodian currency, exchange rates, and tipping culture?' },
  { id: 'sunrise', icon: markRaw(Sun), title: 'Best time for Angkor Wat sunrise', prompt: 'What is the best time and spot for Angkor Wat sunrise?' },
  { id: 'transport', icon: markRaw(Compass), title: 'Travel from Phnom Penh to Siem Reap', prompt: 'How do I travel comfortably between Phnom Penh and Siem Reap?' },
  { id: 'nature', icon: markRaw(MapPin), title: 'Bokor National Park in Kampot', prompt: 'What can I explore at Bokor National Park in Kampot?' }
];

const kmWelcomePromptsPool = [
  { id: 'temples', icon: markRaw(Landmark), title: 'ប្រាសាទល្បីៗក្រៅពីអង្គរវត្ត', prompt: 'តើប្រាសាទល្បីៗណាខ្លះដែលគួរទៅទស្សនាក្រៅពីអង្គរវត្ត?' },
  { id: 'crab', icon: markRaw(Utensils), title: 'ក្តាមឆាម្រេចខ្ចីនៅកែប', prompt: 'តើក្តាមឆាម្រេចខ្ចីនៅកែបមានរសជាតិយ៉ាងណា?' },
  { id: 'itinerary', icon: markRaw(Calendar), title: 'គម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប', prompt: 'រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប' },
  { id: 'beach', icon: markRaw(Palmtree), title: 'ឆ្នេរខ្សាច់ស្អាតបំផុតនៅកោះរ៉ុង', prompt: 'តើឆ្នេរខ្សាច់ណាខ្លះដែលស្អាតបំផុតនៅកោះរ៉ុង?' },
  { id: 'currency', icon: markRaw(Coins), title: 'ការចាយលុយដុល្លារ និងប្រាក់រៀល', prompt: 'តើការចាយលុយដុល្លារ និងប្រាក់រៀលនៅកម្ពុជាត្រូវដឹងអ្វីខ្លះ?' },
  { id: 'sunrise', icon: markRaw(Sun), title: 'ពេលល្អបំផុតមើលថ្ងៃរះនៅអង្គរ', prompt: 'តើពេលវេលាណាដែលល្អបំផុតសម្រាប់មើលថ្ងៃរះនៅប្រាសាទអង្គរវត្ត?' },
  { id: 'transport', icon: markRaw(Compass), title: 'ធ្វើដំណើរពីភ្នំពេញទៅសៀមរាប', prompt: 'តើធ្វើដំណើរពីភ្នំពេញទៅសៀមរាបតាមមធ្យោបាយណាស្រួលជាងគេ?' },
  { id: 'nature', icon: markRaw(MapPin), title: 'កម្សាន្តនៅឧទ្យានជាតិភ្នំបូកគោ', prompt: 'តើនៅឧទ្យានជាតិភ្នំបូកគោមានកន្លែងកម្សាន្តអ្វីខ្លះ?' }
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
    return stored ? JSON.parse(stored) : { name: 'Traveler', email: '', travelStyle: 'cultural', preferredDestinations: ['siem_reap'] };
  } catch (e) {
    return { name: 'Traveler', email: '', travelStyle: 'cultural', preferredDestinations: ['siem_reap'] };
  }
};

const userProfile = ref(getInitialProfile());

watch(userProfile, (newVal) => {
  try {
    localStorage.setItem('cambodia_ai_user_profile', JSON.stringify(newVal));
  } catch (e) {}
}, { deep: true });

// Update document language attribute dynamically
watch(language, (newLang) => {
  try {
    document.documentElement.lang = newLang;
    document.documentElement.setAttribute('data-lang', newLang);
  } catch (e) {}
}, { immediate: true });

// Update current mode state when network changes
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
      localSessions[idx] = newSession;
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

// Switch chat session
const handleSelectSession = async (sessionId) => {
  if (!sessionId) return;
  currentSessionId.value = sessionId;
  localStorage.setItem('aichat_last_active_session_id', sessionId);
  error.value = null;

  // 1. Try server fetch if online
  if (isOnline.value) {
    try {
      const data = await fetchChatSession(sessionId);
      const resData = (data && data.data) ? data.data : data;
      if (resData && resData.messages && Array.isArray(resData.messages) && resData.messages.length > 0) {
        const formattedMsgs = resData.messages.map((m, idx) => ({
          id: m.id || (idx + 1),
          sender: m.sender || (m.role === 'assistant' ? 'ai' : m.role || 'user'),
          message: m.message || m.content || '',
          mode: m.mode || 'online',
          created_at: m.created_at || new Date().toISOString(),
        }));
        messages.value = formattedMsgs;
        if (resData.metadata && resData.metadata.language) {
          language.value = resData.metadata.language;
        }
        return;
      }
    } catch (err) {
      console.warn('Online session fetch failed, checking local sessions:', err);
    }
  }

  // 2. Fallback to localStorage sessions
  try {
    const stored = localStorage.getItem('aichat_local_sessions');
    const localList = stored ? JSON.parse(stored) : [];
    const local = Array.isArray(localList) ? localList.find((s) => s.session_id === sessionId) : null;
    if (local && local.messages && Array.isArray(local.messages)) {
      const formattedMsgs = local.messages.map((m, idx) => ({
        id: m.id || (idx + 1),
        sender: m.sender || (m.role === 'assistant' ? 'ai' : m.role || 'user'),
        message: m.message || m.content || '',
        mode: m.mode || 'offline',
        created_at: m.created_at || new Date().toISOString(),
      }));
      messages.value = formattedMsgs;
      if (local.language) {
        language.value = local.language;
      }
    }
  } catch (e) {
    console.error('Error reading local session backup:', e);
  }
};

// Create New Chat
const handleNewChat = () => {
  currentSessionId.value = null;
  localStorage.removeItem('aichat_last_active_session_id');
  messages.value = [];
  error.value = null;
};

// Clear / Delete all chat history
const handleClearChat = async () => {
  try {
    localStorage.removeItem('aichat_local_sessions');
    localStorage.removeItem('aichat_last_active_session_id');
  } catch (e) {
    console.error('Error clearing local session storage:', e);
  }
  sessions.value = [];
  currentSessionId.value = null;
  messages.value = [];
  error.value = null;

  if (isOnline.value) {
    try {
      await clearAllChatSessions();
    } catch (err) {
      console.warn('Error clearing sessions on server:', err);
    }
  }
};

// Delete single session
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

  if (currentSessionId.value === sessionId || !currentSessionId.value || sessions.value.length <= 1) {
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

// Send Message Handler
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

  try {
    let aiMsg = null;
    let respMode = 'offline';
    let activeSid = currentSessionId.value;

    // 1. Try sending message to FastAPI backend with full session context
    try {
      const historyPayload = messages.value
        .filter((m) => m && (m.message || m.content))
        .map((m) => ({
          role: m.sender === 'user' || m.role === 'user' ? 'user' : 'assistant',
          content: m.message || m.content || '',
        }))
        .slice(-10);

      const response = await sendMessage({
        message: userMessageText,
        language: language.value,
        session_id: currentSessionId.value,
        history: historyPayload,
      });

      const resData = response?.data;
      const apiPayload = (resData && typeof resData === 'object') ? resData : response;

      const answerText =
        apiPayload?.answer ||
        apiPayload?.message_text ||
        (apiPayload?.message && apiPayload.message !== 'Message processed successfully.' ? apiPayload.message : '') ||
        response?.answer ||
        response?.message_text ||
        (response?.message && response.message !== 'Message processed successfully.' ? response.message : '') ||
        '';

      if (response && (response.success || apiPayload) && answerText) {
        const sid = apiPayload?.session_id || response?.session_id || currentSessionId.value || `session_${Date.now()}`;
        if (sid) {
          activeSid = sid;
          currentSessionId.value = sid;
          localStorage.setItem('aichat_last_active_session_id', sid);
        }

        respMode = apiPayload?.mode || response?.mode || (isOnline.value ? 'online' : 'offline');
        currentMode.value = respMode;

        aiMsg = {
          id: Date.now() + 1,
          sender: 'ai',
          message: answerText,
          mode: respMode,
          model: apiPayload?.model || response?.model,
          data_sources: apiPayload?.data_sources || response?.data_sources || [],
          intent: apiPayload?.intent || response?.intent,
          analysis: apiPayload?.analysis,
          summary: apiPayload?.summary,
          sentiment: apiPayload?.sentiment,
          sources: apiPayload?.sources || response?.sources || [],
          suggestions: apiPayload?.suggestions || response?.suggestions || [],
          weather: apiPayload?.weather || response?.weather,
          currency: apiPayload?.currency || response?.currency,
          itinerary: apiPayload?.itinerary || response?.itinerary,
          recommendations: apiPayload?.recommendations || response?.recommendations,
          created_at: new Date().toISOString(),
        };

        if (isOnline.value) loadSessions();
      }
    } catch (err) {
      console.warn('Backend API call unreached. Switching to client-side offline search:', err);
    }

    // 2. Client-side search fallback if backend unreachable
    if (!aiMsg) {
      const offlineRes = await performOfflineSearch(userMessageText, language.value);
      activeSid = activeSid || `off_${Date.now()}`;
      currentSessionId.value = activeSid;
      localStorage.setItem('aichat_last_active_session_id', activeSid);

      aiMsg = {
        id: Date.now() + 1,
        sender: 'ai',
        message: offlineRes.message || 'Angkor Verse AI is ready to help explore Cambodia.',
        mode: 'offline',
        sources: offlineRes.sources || [],
        suggestions: offlineRes.suggestions || [],
        created_at: new Date().toISOString(),
      };
      currentMode.value = 'offline';
    }

    // Append AI response
    if (aiMsg && activeSid) {
      localStorage.setItem('aichat_last_active_session_id', activeSid);
      const updated = [...messages.value, aiMsg];
      messages.value = updated;
      const firstUserMsg = updated.find(m => m.sender === 'user' || m.role === 'user');
      const cleanTitle = firstUserMsg ? firstUserMsg.message : userMessageText;

      saveLocalSession({
        session_id: activeSid,
        title: cleanTitle,
        language: language.value,
        created_at: new Date().toISOString(),
        messages: updated,
      });
    }

  } catch (e) {
    console.error('Error in chat handler:', e);
    error.value = 'Failed to process message.';
  } finally {
    isLoading.value = false;
  }
};

// Regenerate last AI response
const handleRegenerate = async () => {
  if (messages.value.length === 0 || isLoading.value) return;
  // If last message was from AI, pop it so we can re-generate cleanly
  if (messages.value[messages.value.length - 1]?.sender === 'ai') {
    messages.value = messages.value.slice(0, -1);
  }
  const lastUserMsg = [...messages.value].reverse().find((m) => m.sender === 'user' || m.role === 'user');
  if (lastUserMsg && lastUserMsg.message) {
    handleSendMessage(lastUserMsg.message, [], true);
  }
};

// Edit user message and re-generate AI response
const handleEditMessage = async ({ id, newText, index, message: origMsg }) => {
  if (!newText || !newText.trim() || isLoading.value) return;

  let targetIndex = index;
  if (targetIndex === undefined || targetIndex < 0) {
    targetIndex = messages.value.findIndex((m) => m.id === id);
  }
  if (targetIndex === -1) return;

  const attachments = origMsg?.attachments || messages.value[targetIndex]?.attachments || [];

  // Truncate messages back to targetIndex (ChatGPT style)
  messages.value = messages.value.slice(0, targetIndex);

  // Send edited text to generate updated response
  await handleSendMessage(newText.trim(), attachments, false);
};

// Initialize
onMounted(() => {
  loadLocalSessions();
  const lastSessionId = localStorage.getItem('aichat_last_active_session_id');
  if (lastSessionId) {
    handleSelectSession(lastSessionId);
  }

  if (isOnline.value) {
    loadSessions();
  }
});
</script>
