<template>
  <div :class="['flex w-full mb-5', isUser ? 'justify-end' : 'justify-start']">
    
    <!-- Message Content Area -->
    <div :class="['max-w-[85%] sm:max-w-[80%] group relative', isUser ? 'flex flex-col items-end' : 'flex flex-col items-start']">
      
      <!-- Mode Tag Badge for AI -->
      <div v-if="!isUser" class="flex flex-wrap items-center gap-1.5 mb-1 px-1 text-[11px]">
        <span class="font-bold text-slate-900 dark:text-white">Angkor Verse AI</span>
        <span>•</span>
        <span
          v-if="mode === 'offline' || mode === 'degraded' || mode === 'fallback'"
          class="inline-flex items-center gap-1 font-medium px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700 text-[10px]"
        >
          <WifiOff :size="9" /> Offline
        </span>
        <span
          v-else
          class="inline-flex items-center gap-1 font-medium px-2 py-0.5 rounded-full bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60 text-[10px]"
        >
          <Wifi :size="9" /> Online
        </span>
      </div>

      <!-- Message Bubble Container -->
      <div
        :class="[
          'px-4 py-3 rounded-2xl shadow-2xs text-[15px] sm:text-[15.5px]',
          hasKhmer ? 'leading-[1.75]' : 'leading-relaxed',
          isUser
            ? 'bg-[#003E83] dark:bg-[#003E83] text-white rounded-2xl font-normal sm:font-medium shadow-xs shadow-blue-900/15'
            : 'bg-white dark:bg-[#18181b] text-[#111827] dark:text-[#f4f4f5] border border-[#f3f4f6] dark:border-[#27272a] rounded-2xl rounded-tl-xs'
        ]"
      >
        <!-- User Attached Files/Images Preview -->
        <div v-if="isUser && message.attachments && message.attachments.length > 0" class="mb-2 flex flex-wrap gap-1.5">
          <div
            v-for="(att, i) in message.attachments"
            :key="i"
            class="flex items-center space-x-1 bg-white/20 px-2 py-0.5 rounded-md text-xs"
          >
            <ImageIcon :size="12" />
            <span class="truncate max-w-[120px]">{{ att.name }}</span>
          </div>
        </div>

        <!-- User Inline Editing Container -->
        <div v-if="isUser && isEditing" class="w-full min-w-[220px] sm:min-w-[300px]">
          <textarea
            ref="editTextareaRef"
            v-model="editText"
            @input="adjustEditHeight"
            @keydown="handleEditKeyDown"
            rows="2"
            class="w-full bg-transparent text-white placeholder-white/60 focus:outline-none resize-none text-[15px] leading-relaxed py-1"
            :placeholder="isKhmer ? 'បញ្ចូលសារកែប្រែ...' : 'Edit your message...'"
          ></textarea>
          <div class="flex items-center justify-end space-x-2 mt-2 pt-2 border-t border-white/20">
            <button
              type="button"
              @click="cancelEdit"
              class="px-3 py-1 text-xs rounded-full font-medium bg-white/10 hover:bg-white/20 text-white transition-colors cursor-pointer"
            >
              {{ isKhmer ? 'បោះបង់' : 'Cancel' }}
            </button>
            <button
              type="button"
              @click="saveEdit"
              :disabled="!editText.trim()"
              class="px-3 py-1 text-xs rounded-full font-medium bg-white text-slate-900 hover:bg-slate-100 disabled:opacity-50 transition-colors cursor-pointer shadow-xs"
            >
              {{ isKhmer ? 'ផ្ញើ' : 'Send' }}
            </button>
          </div>
        </div>

        <!-- Formatted Text Content -->
        <div v-else class="message-text">
          <span
            v-for="(line, lineIdx) in parsedLines"
            :key="lineIdx"
            :class="['block mb-1', line.isKhmer || hasKhmer ? 'leading-[1.75]' : 'leading-relaxed']"
          >
            <template v-for="(part, pIdx) in line.parts" :key="pIdx">
              <strong v-if="part.isBold" :class="isUser ? 'font-bold text-white' : 'font-bold text-slate-900 dark:text-white'">
                {{ part.text }}
              </strong>
              <template v-else>{{ part.text }}</template>
            </template>
          </span>
        </div>

        <!-- Real-time Weather Widget -->
        <WeatherCard v-if="!isUser && message.weather" :weather="message.weather" :language="language" />

        <!-- Interactive Itinerary Component -->
        <ItineraryCard v-if="!isUser && message.itinerary" :itinerary="message.itinerary" :language="language" />

        <!-- Smart Recommendation Cards -->
        <RecommendationCard
          v-if="!isUser && !message.itinerary && message.recommendations && message.recommendations.length > 0"
          :recommendations="message.recommendations"
          :language="language"
        />

        <!-- Currency Card -->
        <CurrencyCard v-if="!isUser && message.currency" :currency="message.currency" :language="language" />

        <!-- Matched Database Source Cards -->
        <div
          v-if="!isUser && !hasSpecializedCard && message.sources && message.sources.length > 0"
          class="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800 space-y-1.5"
        >
          <p class="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
            {{ isKhmer ? 'ប្រភពទិន្នន័យទេសចរណ៍៖' : 'Tourism Database Source:' }}
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <div
              v-for="(src, idx) in message.sources.slice(0, 2)"
              :key="idx"
              class="bg-slate-50/80 dark:bg-slate-900/70 border border-slate-200 dark:border-slate-700 rounded-xl p-2.5 text-xs hover:border-[#003E83] dark:hover:border-blue-500 transition-colors"
            >
              <div class="flex items-center justify-between gap-1 mb-1">
                <h4 class="font-bold text-slate-900 dark:text-white text-xs truncate">
                  {{ src.name || src.title || 'Cambodia Destination' }}
                </h4>
                <span
                  v-if="src.category || src.type"
                  class="bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[9px] uppercase font-semibold px-1.5 py-0.5 rounded-md shrink-0"
                >
                  {{ src.category || src.type }}
                </span>
              </div>
              <div v-if="src.location || src.province" class="flex items-center text-[10px] text-slate-500 dark:text-slate-400 mb-0.5">
                <MapPin :size="10" class="text-[#003E83] dark:text-[#2563eb] mr-1 shrink-0" />
                <span class="truncate">{{ src.location || src.province }}</span>
              </div>
              <div v-if="src.google_maps_url" class="mt-1 pt-1 border-t border-slate-200/60 dark:border-slate-800 flex justify-end">
                <a
                  :href="src.google_maps_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-flex items-center gap-0.5 text-[9px] font-bold text-[#003E83] dark:text-blue-400 hover:underline"
                >
                  <span>{{ isKhmer ? 'មើលផែនទី' : 'Maps' }}</span>
                  <ExternalLink :size="8" />
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Contextual Suggestions Chips -->
        <div
          v-if="!isUser && isLatest && currentSuggestions && currentSuggestions.length > 0"
          class="mt-2.5 pt-2 border-t border-slate-100 dark:border-slate-800/80"
        >
          <div class="flex items-center justify-between mb-1.5 px-0.5">
            <p class="inline-flex items-center gap-1.5 text-[10px] font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
              <Sparkles :size="11" class="text-amber-500 shrink-0" />
              <span>{{ isKhmer ? 'សំណើបន្ថែម៖' : 'Suggested Questions:' }}</span>
            </p>
            <button
              type="button"
              @click.stop="refreshSuggestions"
              class="inline-flex items-center gap-1 text-[11px] font-medium text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 px-2 py-0.5 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-all cursor-pointer group active:scale-95"
              :title="isKhmer ? 'ប្តូរសំណួរថ្មី' : 'Refresh questions'"
            >
              <RotateCcw
                :size="11"
                :class="['transition-transform duration-500', isRefreshingSuggestions ? '-rotate-180 text-blue-600 dark:text-blue-400' : 'group-hover:-rotate-90']"
              />
              <span>{{ isKhmer ? 'ប្តូរសំណួរ' : 'Refresh' }}</span>
            </button>
          </div>

          <div class="flex flex-wrap gap-1.5">
            <button
              v-for="(suggestion, sIdx) in currentSuggestions"
              :key="sIdx"
              @click="$emit('select-suggestion', suggestion)"
              class="inline-flex items-center gap-1.5 text-left text-xs bg-slate-50 dark:bg-slate-800/80 hover:bg-blue-50 dark:hover:bg-blue-950/40 text-slate-700 dark:text-slate-300 hover:text-[#003E83] dark:hover:text-blue-400 border border-slate-200 dark:border-slate-700 hover:border-blue-300 dark:hover:border-blue-800 rounded-full px-3 py-1.5 transition-all duration-150 shadow-2xs cursor-pointer active:scale-95 group"
            >
              <Compass :size="12" class="text-blue-600 dark:text-blue-400 shrink-0 group-hover:rotate-45 transition-transform" />
              <span>{{ suggestion }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- User Message Actions Toolbar (Copy & Edit, as seen in Picture 1) -->
      <div
        v-if="isUser && !isEditing"
        class="flex items-center justify-end space-x-1.5 mt-1 px-1 text-slate-400 dark:text-zinc-400"
      >
        <!-- Copy Button -->
        <button
          @click="handleCopy"
          class="flex items-center p-1 rounded-md hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-zinc-800 transition-colors cursor-pointer text-xs"
          :title="copied ? (isKhmer ? 'បានចម្លង!' : 'Copied!') : (isKhmer ? 'ចម្លង' : 'Copy')"
        >
          <template v-if="copied">
            <Check :size="13" class="text-blue-500 dark:text-blue-400" />
            <span class="text-blue-600 dark:text-blue-400 text-[10px] font-semibold ml-1">
              {{ isKhmer ? 'បានចម្លង' : 'Copied' }}
            </span>
          </template>
          <Copy v-else :size="13" />
        </button>

        <!-- Edit Button -->
        <button
          @click="startEdit"
          class="p-1 rounded-md hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-zinc-800 transition-colors cursor-pointer text-xs"
          :title="isKhmer ? 'កែប្រែសារ' : 'Edit message'"
        >
          <Pencil :size="13" />
        </button>
      </div>

      <!-- AI Message Actions Toolbar -->
      <div v-if="!isUser" class="flex items-center space-x-1 mt-1 text-slate-400 dark:text-slate-500">
        <button
          @click="handleCopy"
          class="flex items-center space-x-1 p-1 rounded-md hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer text-xs"
          :title="copied ? 'Copied!' : 'Copy response'"
        >
          <template v-if="copied">
            <Check :size="12" class="text-blue-500" />
            <span class="text-blue-600 dark:text-blue-400 text-[10px] font-semibold">
              {{ isKhmer ? 'បានចម្លង' : 'Copied' }}
            </span>
          </template>
          <Copy v-else :size="12" />
        </button>

        <button
          @click="$emit('regenerate')"
          class="p-1 rounded-md hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors cursor-pointer"
          title="Regenerate response"
        >
          <RotateCcw :size="12" />
        </button>

        <button
          @click="handleFeedback('like')"
          :class="[
            'p-1 rounded-md transition-colors cursor-pointer',
            feedback === 'like'
              ? 'text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/40'
              : 'hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'
          ]"
          title="Good response"
        >
          <ThumbsUp :size="12" />
        </button>

        <button
          @click="handleFeedback('dislike')"
          :class="[
            'p-1 rounded-md transition-colors cursor-pointer',
            feedback === 'dislike'
              ? 'text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40'
              : 'hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'
          ]"
          title="Poor response"
        >
          <ThumbsDown :size="12" />
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue';
import {
  Copy, Check, Pencil, MapPin, ThumbsUp, ThumbsDown, RotateCcw,
  Wifi, WifiOff, Image as ImageIcon, ExternalLink, Sparkles, Compass
} from 'lucide-vue-next';
import ItineraryCard from './ItineraryCard.vue';
import WeatherCard from './WeatherCard.vue';
import RecommendationCard from './RecommendationCard.vue';
import CurrencyCard from '../cards/CurrencyCard.vue';

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  language: {
    type: String,
    default: 'en',
  },
  isLatest: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['regenerate', 'select-suggestion', 'edit-message']);

const copied = ref(false);
const feedback = ref(null);
const isEditing = ref(false);
const editText = ref('');
const editTextareaRef = ref(null);

const isUser = computed(() => props.message.sender === 'user' || props.message.role === 'user');
const isKhmer = computed(() => props.language === 'km');
const mode = computed(() => props.message.mode || 'online');
const textContent = computed(() => props.message.message || props.message.content || '');
const hasKhmer = computed(() => isKhmer.value || /[\u1780-\u17FF]/.test(textContent.value));

const hasSpecializedCard = computed(() => {
  return Boolean(
    props.message.itinerary ||
    (props.message.recommendations && props.message.recommendations.length > 0) ||
    props.message.currency
  );
});

const parsedLines = computed(() => {
  const text = textContent.value;
  if (!text) return [];

  return text.split('\n').map((line) => {
    const isLineKhmer = /[\u1780-\u17FF]/.test(line);
    const partsRaw = line.split(/(\*\*.*?\*\*)/g);
    const parts = partsRaw.map((part) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return { isBold: true, text: part.slice(2, -2) };
      }
      return { isBold: false, text: part };
    });
    return { isKhmer: isLineKhmer, parts };
  });
});

const enSuggestionsPool = [
  'What must-see temples in Siem Reap should I visit besides Angkor Wat?',
  'Tell me about fresh Kampot pepper crab in Kep',
  'How much does an Angkor Wat temple pass cost?',
  'What authentic Khmer dishes are must-try in Cambodia?',
  'Create a 3-day Siem Reap cultural itinerary',
  'What is the dress code for visiting ancient temples in Cambodia?',
  'What are the most beautiful beaches on Koh Rong island?',
  'What is the best time and spot for Angkor Wat sunrise?',
  'How do I travel comfortably between Phnom Penh and Siem Reap?',
  'Where can I find the best Fish Amok and Beef Lok Lak?',
  'What is the current USD to Cambodian Riel exchange rate?',
  'What can I explore at Bokor National Park in Kampot?',
  'What are the top highlights of the Royal Palace in Phnom Penh?',
  'What should I know about Cambodian currency and tipping culture?',
  'How do PassApp and Grab tuk-tuks work in Cambodia?',
  'What traditional festivals and holidays happen in Cambodia?',
  'Can you suggest a relaxing 2-day beach getaway itinerary?',
  'Tell me about the hidden jungle temple of Beng Mealea',
  'What is the best time of year to visit Cambodia for good weather?',
  'What are the best sunset viewpoints around Siem Reap and Tonle Sap?',
  'What are some respectful cultural etiquettes to follow in Cambodia?',
  'Where can I experience an authentic Apsara dance performance?'
];

const kmSuggestionsPool = [
  'តើប្រាសាទល្បីៗណាខ្លះដែលគួរទៅទស្សនាក្រៅពីអង្គរវត្ត?',
  'តើក្តាមឆាម្រេចខ្ចីនៅកែបមានរសជាតិយ៉ាងណា?',
  'តើតម្លៃសំបុត្រចូលទស្សនាអង្គរវត្តប៉ុន្មានដែរ?',
  'តើម្ហូបខ្មែរប្រពៃណីណាខ្លះដែលមិនគួររំលង?',
  'រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប',
  'តើត្រូវស្លៀកពាក់បែបណាពេលចូលទស្សនាប្រាសាទបុរាណ?',
  'តើឆ្នេរខ្សាច់ណាខ្លះដែលស្អាតបំផុតនៅកោះរ៉ុង?',
  'តើពេលវេលាណាដែលល្អបំផុតសម្រាប់មើលថ្ងៃរះនៅប្រាសាទអង្គរវត្ត?',
  'តើធ្វើដំណើរពីភ្នំពេញទៅសៀមរាបតាមមធ្យោបាយណាស្រួលជាងគេ?',
  'តើអាចរកញ៉ាំអាម៉ុកត្រី និងឡុកឡាក់ឆ្ងាញ់នៅឯណា?',
  'តើអត្រាប្តូរប្រាក់ ១ ដុល្លារស្មើនឹងប៉ុន្មានរៀលថ្ងៃនេះ?',
  'តើនៅឧទ្យានជាតិភ្នំបូកគោមានកន្លែងកម្សាន្តអ្វីខ្លះ?',
  'តើព្រះបរមរាជវាំងនៅភ្នំពេញមានអ្វីពិសេសខ្លះ?',
  'តើការចាយលុយដុល្លារ និងប្រាក់រៀលនៅកម្ពុជាត្រូវដឹងអ្វីខ្លះ?',
  'តើការប្រើប្រាស់ PassApp និង Grab នៅកម្ពុជាយ៉ាងដូចម្តេច?',
  'តើពិធីបុណ្យប្រពៃណីខ្មែរល្បីៗមានអ្វីខ្លះពេញមួយឆ្នាំ?',
  'រៀបចំគម្រោងលំហែកាយ ២ ថ្ងៃនៅឆ្នេរសមុទ្រកោះរ៉ុង',
  'តើប្រាសាទបេងមាលាមានប្រវត្តិ និងភាពទាក់ទាញយ៉ាងណា?',
  'តើរដូវកាលណាដែលល្អបំផុតសម្រាប់មកកម្សាន្តនៅកម្ពុជា?',
  'តើកន្លែងណាខ្លះដែលល្អបំផុតសម្រាប់មើលថ្ងៃលិចនៅបឹងទន្លេសាប?',
  'តើមានទំនៀមទម្លាប់អ្វីខ្លះដែលភ្ញៀវទេសចរគួរយល់ដឹងនៅកម្ពុជា?',
  'តើអាចទស្សនារបាំព្រះរាជទ្រព្យ (អប្សរា) នៅទីណាបាន?'
];

const currentSuggestions = ref([]);
const isRefreshingSuggestions = ref(false);

const getFreshSuggestions = (exclude = []) => {
  if (isUser.value) return [];
  const isKm = hasKhmer.value || isKhmer.value;
  const pool = isKm ? kmSuggestionsPool : enSuggestionsPool;

  const backendSuggestions = props.message.suggestions || [];
  const combined = Array.from(new Set([...backendSuggestions, ...pool]));

  // Exclude current suggestions so refreshed questions are NOT the same
  const available = combined.filter((q) => !exclude.includes(q));
  const poolToUse = available.length >= 3 ? available : combined;

  // Shuffle randomly
  const shuffled = [...poolToUse].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, 3);
};

const refreshSuggestions = () => {
  isRefreshingSuggestions.value = true;
  currentSuggestions.value = getFreshSuggestions(currentSuggestions.value);
  setTimeout(() => {
    isRefreshingSuggestions.value = false;
  }, 400);
};

watch(
  () => [props.message.suggestions, props.language, hasKhmer.value],
  () => {
    if (!isUser.value) {
      currentSuggestions.value = getFreshSuggestions();
    }
  },
  { immediate: true }
);

const handleCopy = () => {
  navigator.clipboard.writeText(textContent.value);
  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 2000);
};

const handleFeedback = (type) => {
  feedback.value = feedback.value === type ? null : type;
};

const startEdit = () => {
  editText.value = textContent.value;
  isEditing.value = true;
  nextTick(() => {
    if (editTextareaRef.value) {
      editTextareaRef.value.focus();
      adjustEditHeight();
    }
  });
};

const cancelEdit = () => {
  isEditing.value = false;
  editText.value = '';
};

const adjustEditHeight = () => {
  nextTick(() => {
    if (editTextareaRef.value) {
      editTextareaRef.value.style.height = 'auto';
      editTextareaRef.value.style.height = `${Math.min(editTextareaRef.value.scrollHeight, 220)}px`;
    }
  });
};

const handleEditKeyDown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    saveEdit();
  } else if (e.key === 'Escape') {
    cancelEdit();
  }
};

const saveEdit = () => {
  const trimmed = editText.value.trim();
  if (!trimmed) return;
  emit('edit-message', {
    id: props.message.id,
    newText: trimmed,
    message: props.message,
  });
  isEditing.value = false;
};
</script>
