<template>
  <div :class="['flex items-start space-x-3 mb-5', isUser ? 'flex-row-reverse space-x-reverse' : '']">
    
    <!-- Avatar -->
    <div
      :class="[
        'w-8 h-8 rounded-xl flex items-center justify-center shrink-0 shadow-xs overflow-hidden',
        isUser
          ? 'bg-[#003E83] text-white'
          : 'bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700'
      ]"
    >
      <User v-if="isUser" :size="16" />
      <img
        v-else
        src="/tourism_logo.png"
        alt="Angkor Verse AI"
        class="w-full h-full object-contain p-0.5 rounded-xl"
      />
    </div>

    <!-- Message Content Area -->
    <div :class="['max-w-[85%] sm:max-w-[80%] group relative', isUser ? 'items-end' : 'items-start']">
      
      <!-- Mode Tag Badge for AI -->
      <div v-if="!isUser" class="flex flex-wrap items-center gap-1.5 mb-1 px-1 text-[11px]">
        <span class="font-bold text-slate-900 dark:text-white">Angkor Verse AI</span>
        <span>•</span>
        <span
          v-if="mode === 'offline' || mode === 'degraded' || mode === 'fallback'"
          class="inline-flex items-center gap-1 font-medium px-2 py-0.2 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700 text-[10px]"
        >
          <WifiOff :size="9" /> Offline
        </span>
        <span
          v-else
          class="inline-flex items-center gap-1 font-medium px-2 py-0.2 rounded-full bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60 text-[10px]"
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
            ? 'bg-[#003E83] text-white rounded-tr-xs font-medium'
            : 'bg-white dark:bg-[#18181b] text-[#111827] dark:text-[#f4f4f5] border border-[#f3f4f6] dark:border-[#27272a] rounded-tl-xs'
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

        <!-- Formatted Text Content -->
        <div class="message-text">
          <span
            v-for="(line, lineIdx) in parsedLines"
            :key="lineIdx"
            :class="['block mb-1', line.isKhmer || hasKhmer ? 'leading-[1.75]' : 'leading-relaxed']"
          >
            <template v-for="(part, pIdx) in line.parts" :key="pIdx">
              <strong v-if="part.isBold" class="font-bold text-slate-900 dark:text-white">
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
                  class="bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-[9px] uppercase font-semibold px-1.5 py-0.2 rounded-md shrink-0"
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
          v-if="!isUser && displayedSuggestions && displayedSuggestions.length > 0"
          class="mt-2.5 pt-2 border-t border-slate-100 dark:border-slate-800/80"
        >
          <p class="text-[10px] font-semibold text-slate-400 dark:text-slate-500 mb-1.5 uppercase tracking-wider">
            {{ isKhmer ? 'សំណើបន្ថែម៖' : 'Suggested Questions:' }}
          </p>
          <div class="flex flex-wrap gap-1.5">
            <button
              v-for="(suggestion, sIdx) in displayedSuggestions"
              :key="sIdx"
              @click="$emit('select-suggestion', suggestion)"
              class="text-left text-xs bg-slate-50 dark:bg-slate-800/80 hover:bg-blue-50 dark:hover:bg-blue-950/40 text-slate-700 dark:text-slate-300 hover:text-[#003E83] dark:hover:text-blue-400 border border-slate-200 dark:border-slate-700 hover:border-blue-300 dark:hover:border-blue-800 rounded-full px-3 py-1 transition-all duration-150 shadow-2xs cursor-pointer active:scale-95"
            >
              💡 {{ suggestion }}
            </button>
          </div>
        </div>
      </div>

      <!-- Message Actions Toolbar -->
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
import { ref, computed } from 'vue';
import {
  User, Copy, Check, MapPin, ThumbsUp, ThumbsDown, RotateCcw,
  Wifi, WifiOff, Image as ImageIcon, ExternalLink
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
});

defineEmits(['regenerate', 'select-suggestion']);

const copied = ref(false);
const feedback = ref(null);

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

const displayedSuggestions = computed(() => {
  if (isUser.value) return [];
  if (props.message.suggestions && props.message.suggestions.length >= 3) {
    return props.message.suggestions.slice(0, 4);
  }

  const defaultEn = [
    'What are the top attractions to visit in Siem Reap?',
    'Create a 3-day Siem Reap cultural itinerary',
    'What authentic Khmer dishes are must-try in Cambodia?',
    'What is the weather like in Siem Reap today?',
    'What is the current USD to Cambodian Riel exchange rate?',
    'What are the most beautiful beaches on Koh Rong?',
    'How much does an Angkor Wat temple pass cost?',
    'How do I travel comfortably between Phnom Penh and Siem Reap?'
  ];

  const defaultKm = [
    'តើកន្លែងណាខ្លះគួរទៅកម្សាន្តនៅសៀមរាប?',
    'រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប',
    'តើម្ហូបខ្មែរប្រពៃណីណាខ្លះដែលមិនគួររំលង?',
    'តើអាកាសធាតុនៅសៀមរាបថ្ងៃនេះយ៉ាងណាដែរ?',
    'តើអត្រាប្តូរប្រាក់ ១ ដុល្លារស្មើនឹងប៉ុន្មានរៀលថ្ងៃនេះ?',
    'តើឆ្នេរខ្សាច់ណាខ្លះដែលស្អាតបំផុតនៅកោះរ៉ុង?',
    'តើតម្លៃសំបុត្រចូលទស្សនាអង្គរវត្តប៉ុន្មានដែរ?',
    'តើធ្វើដំណើរពីភ្នំពេញទៅសៀមរាបតាមមធ្យោបាយណាស្រួលជាងគេ?'
  ];

  const existing = props.message.suggestions || [];
  const pool = hasKhmer.value || isKhmer.value ? defaultKm : defaultEn;
  const additional = pool.filter(p => !existing.includes(p)).sort(() => 0.5 - Math.random());
  const combined = [...existing, ...additional];
  const targetCount = 3;
  return combined.slice(0, targetCount);
});

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
</script>
