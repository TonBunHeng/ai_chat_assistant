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
            : 'bg-white dark:bg-[#18181b] text-[#111827] dark:text-[#f4f4f5] border border-[#f3f4f6] dark:border-[#27272a] rounded-2xl rounded-tl-xs w-full'
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

        <!-- Matched AI Grounded Source Cards -->
        <div
          v-if="!isUser && !hasSpecializedCard && message.sources && message.sources.length > 0"
          class="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800 space-y-1.5"
        >
          <div class="flex items-center justify-between px-0.5">
            <p class="inline-flex items-center gap-1.5 text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
              <Sparkles :size="11" class="text-amber-500 shrink-0" />
              <span>{{ isKhmer ? 'ប្រភពយោង AI ទេសចរណ៍៖' : 'AI Tourism Source:' }}</span>
            </p>
            <span class="inline-flex items-center gap-1 text-[9px] font-semibold text-[#003E83] dark:text-blue-400 bg-blue-50 dark:bg-blue-950/40 px-1.5 py-0.5 rounded-full border border-blue-200/60 dark:border-blue-800/50">
              <span>AI Grounded</span>
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <div
              v-for="(src, idx) in message.sources.slice(0, 2)"
              :key="idx"
              class="bg-slate-50/80 dark:bg-[#212121] border border-slate-200/90 dark:border-zinc-800 rounded-xl p-2.5 text-xs hover:border-[#003E83] dark:hover:border-blue-500 transition-colors shadow-2xs"
            >
              <div class="flex items-center justify-between gap-1 mb-1">
                <h4 class="font-bold text-slate-900 dark:text-white text-xs truncate">
                  {{ src.name || src.title || 'Cambodia Destination' }}
                </h4>
                <span
                  v-if="src.category || src.type"
                  class="bg-blue-50 dark:bg-blue-950/40 text-[#003E83] dark:text-blue-300 text-[9px] uppercase font-semibold px-1.5 py-0.5 rounded-md shrink-0 border border-blue-200/60 dark:border-blue-800/50"
                >
                  {{ src.category || src.type }}
                </span>
              </div>
              <div v-if="src.location || src.province" class="flex items-center text-[10px] text-slate-500 dark:text-slate-400 mb-0.5">
                <MapPin :size="10" class="text-[#003E83] dark:text-[#2563eb] mr-1 shrink-0" />
                <span class="truncate">{{ src.location || src.province }}</span>
              </div>
              <div v-if="src.google_maps_url" class="mt-1 pt-1 border-t border-slate-200/60 dark:border-zinc-800 flex justify-end">
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

        <!-- Contextual Suggested Topics Grid (Matching Picture 2) -->
        <div
          v-if="!isUser && isLatest && currentSuggestions && currentSuggestions.length > 0"
          class="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800/80 w-full"
        >
          <div class="flex items-center justify-between mb-2 px-1">
            <span class="text-[11px] font-semibold text-slate-400 dark:text-zinc-500 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles :size="12" class="text-amber-500" />
              <span>{{ isKhmer ? 'សំណើណែនាំ' : 'Suggested Topics' }}</span>
            </span>
            <button
              type="button"
              @click.stop="refreshSuggestions"
              class="inline-flex items-center gap-1.5 text-[11px] font-medium text-slate-500 dark:text-zinc-400 hover:text-[#003E83] dark:hover:text-blue-400 px-2 py-0.5 rounded-full hover:bg-slate-100 dark:hover:bg-zinc-800 transition-all cursor-pointer group active:scale-95"
              :title="isKhmer ? 'ប្តូរសំណួរថ្មី' : 'Refresh questions'"
            >
              <RotateCcw
                :size="11"
                :class="['transition-transform duration-500', isRefreshingSuggestions ? '-rotate-180 text-[#003E83] dark:text-blue-400' : 'group-hover:-rotate-90']"
              />
              <span>{{ isKhmer ? 'ប្តូរសំណួរ' : 'Refresh' }}</span>
            </button>
          </div>

          <!-- Suggested Topic Cards Grid (2x2 matching Picture 2) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <button
              v-for="(card, cIdx) in currentSuggestions"
              :key="cIdx"
              @click="$emit('select-suggestion', card.prompt || card.title)"
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
import { ref, computed, nextTick, watch, markRaw } from 'vue';
import {
  Copy, Check, Pencil, MapPin, ThumbsUp, ThumbsDown, RotateCcw,
  Wifi, WifiOff, Image as ImageIcon, ExternalLink, Sparkles, Compass,
  Landmark, Utensils, Calendar, Palmtree, Coins, Sun
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

const enTopicsPool = [
  { id: 'currency', icon: markRaw(Coins), title: 'Currency & USD vs Riel tips', prompt: 'What should I know about Cambodian currency, exchange rates, and tipping culture?' },
  { id: 'itinerary', icon: markRaw(Calendar), title: '3-Day Siem Reap cultural itinerary', prompt: 'Create a 3-day Siem Reap cultural itinerary' },
  { id: 'crab', icon: markRaw(Utensils), title: 'Fresh Kampot pepper crab in Kep', prompt: 'Tell me about fresh Kampot pepper crab in Kep' },
  { id: 'nature', icon: markRaw(MapPin), title: 'Bokor National Park in Kampot', prompt: 'What can I explore at Bokor National Park in Kampot?' },
  { id: 'temples', icon: markRaw(Landmark), title: 'Must-see temples beyond Angkor', prompt: 'What must-see temples in Siem Reap should I visit besides Angkor Wat?' },
  { id: 'beach', icon: markRaw(Palmtree), title: 'Best white sand beaches on Koh Rong', prompt: 'What are the most beautiful beaches on Koh Rong island?' },
  { id: 'sunrise', icon: markRaw(Sun), title: 'Best time for Angkor Wat sunrise', prompt: 'What is the best time and spot for Angkor Wat sunrise?' },
  { id: 'transport', icon: markRaw(Compass), title: 'Travel from Phnom Penh to Siem Reap', prompt: 'How do I travel comfortably between Phnom Penh and Siem Reap?' },
  { id: 'food', icon: markRaw(Utensils), title: 'Must-try authentic Khmer dishes', prompt: 'What authentic Khmer dishes are must-try in Cambodia?' },
  { id: 'amok', icon: markRaw(Utensils), title: 'Best Fish Amok and Beef Lok Lak', prompt: 'Where can I find the best Fish Amok and Beef Lok Lak?' },
  { id: 'pass', icon: markRaw(Coins), title: 'Angkor Wat temple pass prices', prompt: 'How much does an Angkor Wat temple pass cost?' },
  { id: 'palace', icon: markRaw(Landmark), title: 'Royal Palace in Phnom Penh', prompt: 'What are the top highlights of the Royal Palace in Phnom Penh?' },
  { id: 'weather', icon: markRaw(Sun), title: 'Best season & weather in Cambodia', prompt: 'What is the best time of year to visit Cambodia for good weather?' },
  { id: 'sunset', icon: markRaw(Sun), title: 'Tonle Sap sunset viewpoints', prompt: 'What are the best sunset viewpoints around Siem Reap and Tonle Sap?' },
  { id: 'etiquette', icon: markRaw(Compass), title: 'Cambodian cultural etiquette', prompt: 'What are some respectful cultural etiquettes to follow in Cambodia?' },
  { id: 'tuktuk', icon: markRaw(Compass), title: 'PassApp & Grab tuk-tuks guide', prompt: 'How do PassApp and Grab tuk-tuks work in Cambodia?' }
];

const kmTopicsPool = [
  { id: 'currency', icon: markRaw(Coins), title: 'ការចាយលុយដុល្លារ និងប្រាក់រៀល', prompt: 'តើការចាយលុយដុល្លារ និងប្រាក់រៀលនៅកម្ពុជាត្រូវដឹងអ្វីខ្លះ?' },
  { id: 'itinerary', icon: markRaw(Calendar), title: 'គម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប', prompt: 'រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប' },
  { id: 'crab', icon: markRaw(Utensils), title: 'ក្តាមឆាម្រេចខ្ចីនៅកែប', prompt: 'តើក្តាមឆាម្រេចខ្ចីនៅកែបមានរសជាតិយ៉ាងណា?' },
  { id: 'nature', icon: markRaw(MapPin), title: 'កម្សាន្តនៅឧទ្យានជាតិភ្នំបូកគោ', prompt: 'តើនៅឧទ្យានជាតិភ្នំបូកគោមានកន្លែងកម្សាន្តអ្វីខ្លះ?' },
  { id: 'temples', icon: markRaw(Landmark), title: 'ប្រាសាទល្បីៗក្រៅពីអង្គរវត្ត', prompt: 'តើប្រាសាទល្បីៗណាខ្លះដែលគួរទៅទស្សនាក្រៅពីអង្គរវត្ត?' },
  { id: 'beach', icon: markRaw(Palmtree), title: 'ឆ្នេរខ្សាច់ស្អាតបំផុតនៅកោះរ៉ុង', prompt: 'តើឆ្នេរខ្សាច់ណាខ្លះដែលស្អាតបំផុតនៅកោះរ៉ុង?' },
  { id: 'sunrise', icon: markRaw(Sun), title: 'ពេលល្អបំផុតមើលថ្ងៃរះនៅអង្គរ', prompt: 'តើពេលវេលាណាដែលល្អបំផុតសម្រាប់មើលថ្ងៃរះនៅប្រាសាទអង្គរវត្ត?' },
  { id: 'transport', icon: markRaw(Compass), title: 'ធ្វើដំណើរពីភ្នំពេញទៅសៀមរាប', prompt: 'តើធ្វើដំណើរពីភ្នំពេញទៅសៀមរាបតាមមធ្យោបាយណាស្រួលជាងគេ?' },
  { id: 'food', icon: markRaw(Utensils), title: 'ម្ហូបខ្មែរប្រពៃណីមិនគួររំលង', prompt: 'តើម្ហូបខ្មែរប្រពៃណីណាខ្លះដែលមិនគួររំលង?' },
  { id: 'amok', icon: markRaw(Utensils), title: 'អាម៉ុកត្រី និងឡុកឡាក់ឆ្ងាញ់', prompt: 'តើអាចរកញ៉ាំអាម៉ុកត្រី និងឡុកឡាក់ឆ្ងាញ់នៅឯណា?' },
  { id: 'pass', icon: markRaw(Coins), title: 'តម្លៃសំបុត្រចូលអង្គរវត្ត', prompt: 'តើតម្លៃសំបុត្រចូលទស្សនាអង្គរវត្តប៉ុន្មានដែរ?' },
  { id: 'palace', icon: markRaw(Landmark), title: 'ព្រះបរមរាជវាំងនៅភ្នំពេញ', prompt: 'តើព្រះបរមរាជវាំងនៅភ្នំពេញមានអ្វីពិសេសខ្លះ?' },
  { id: 'weather', icon: markRaw(Sun), title: 'រដូវកាលល្អសម្រាប់ដំណើរកម្សាន្ត', prompt: 'តើរដូវកាលណាដែលល្អបំផុតសម្រាប់មកកម្សាន្តនៅកម្ពុជា?' },
  { id: 'sunset', icon: markRaw(Sun), title: 'កន្លែងមើលថ្ងៃលិចនៅទន្លេសាប', prompt: 'តើកន្លែងណាខ្លះដែលល្អបំផុតសម្រាប់មើលថ្ងៃលិចនៅបឹងទន្លេសាប?' },
  { id: 'etiquette', icon: markRaw(Compass), title: 'ទំនៀមទម្លាប់គួរដឹងនៅកម្ពុជា', prompt: 'តើមានទំនៀមទម្លាប់អ្វីខ្លះដែលភ្ញៀវទេសចរគួរយល់ដឹងនៅកម្ពុជា?' },
  { id: 'tuktuk', icon: markRaw(Compass), title: 'ការប្រើប្រាស់ PassApp និង Grab', prompt: 'តើការប្រើប្រាស់ PassApp និង Grab នៅកម្ពុជាយ៉ាងដូចម្តេច?' }
];

const formatTopic = (item) => {
  if (!item) return null;
  if (typeof item === 'object' && item.title && item.icon) return item;

  const str = String(item).trim();
  const isKm = hasKhmer.value || isKhmer.value;
  const pool = isKm ? kmTopicsPool : enTopicsPool;

  const matched = pool.find(p => p.prompt === str || p.title === str || str.toLowerCase().includes(p.title.toLowerCase()));
  if (matched) return matched;

  const s = str.toLowerCase();
  let icon = markRaw(Compass);
  if (s.includes('temple') || s.includes('angkor') || s.includes('palace') || s.includes('ប្រាសាទ') || s.includes('វាំង') || s.includes('វត្ត')) {
    icon = markRaw(Landmark);
  } else if (s.includes('crab') || s.includes('food') || s.includes('amok') || s.includes('dish') || s.includes('lok lak') || s.includes('eat') || s.includes('restaurant') || s.includes('ម្ហូប') || s.includes('ញ៉ាំ') || s.includes('ក្តាម')) {
    icon = markRaw(Utensils);
  } else if (s.includes('itinerary') || s.includes('day') || s.includes('festival') || s.includes('គម្រោង') || s.includes('ថ្ងៃ') || s.includes('បុណ្យ')) {
    icon = markRaw(Calendar);
  } else if (s.includes('beach') || s.includes('island') || s.includes('koh rong') || s.includes('sea') || s.includes('កោះ') || s.includes('ឆ្នេរ') || s.includes('សមុទ្រ')) {
    icon = markRaw(Palmtree);
  } else if (s.includes('currency') || s.includes('usd') || s.includes('riel') || s.includes('rate') || s.includes('cost') || s.includes('price') || s.includes('tip') || s.includes('budget') || s.includes('ដុល្លារ') || s.includes('រៀល') || s.includes('តម្លៃ') || s.includes('ថ្លៃ')) {
    icon = markRaw(Coins);
  } else if (s.includes('sunrise') || s.includes('sunset') || s.includes('weather') || s.includes('season') || s.includes('sun') || s.includes('ថ្ងៃរះ') || s.includes('ថ្ងៃលិច') || s.includes('អាកាសធាតុ')) {
    icon = markRaw(Sun);
  } else if (s.includes('park') || s.includes('bokor') || s.includes('mountain') || s.includes('nature') || s.includes('place') || s.includes('spot') || s.includes('destination') || s.includes('ឧទ្យាន') || s.includes('បូកគោ') || s.includes('ភ្នំ')) {
    icon = markRaw(MapPin);
  }

  let title = str
    .replace(/^(What is the best time and spot for |What is the best time of year to visit |What is the best |What are the top |What are the |What authentic |What should I know about |Tell me about |How do I travel |How much does |Can you suggest |Where can I |Where do I |Create a |តើ|រៀបចំ)/i, '')
    .replace(/\?$/, '')
    .trim();
  if (!title) title = str;

  return {
    id: str,
    icon,
    title,
    prompt: str
  };
};

const currentSuggestions = ref([]);
const isRefreshingSuggestions = ref(false);

const getFreshSuggestions = (excludeIds = []) => {
  if (isUser.value) return [];
  const isKm = hasKhmer.value || isKhmer.value;
  const pool = isKm ? kmTopicsPool : enTopicsPool;

  const rawBackend = (props.message.suggestions || []).map(formatTopic).filter(Boolean);

  const allCandidates = [];
  const seenIds = new Set();

  for (const item of [...rawBackend, ...pool]) {
    const key = item.id || item.title;
    if (!seenIds.has(key)) {
      seenIds.add(key);
      allCandidates.push(item);
    }
  }

  const available = allCandidates.filter(item => !excludeIds.includes(item.id || item.title));
  const poolToUse = available.length >= 4 ? available : allCandidates;

  const shuffled = [...poolToUse].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, 4);
};

const refreshSuggestions = () => {
  isRefreshingSuggestions.value = true;
  const currentIds = currentSuggestions.value.map(c => c.id || c.title);
  currentSuggestions.value = getFreshSuggestions(currentIds);
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
