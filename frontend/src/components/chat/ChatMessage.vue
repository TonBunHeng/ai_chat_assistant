<template>
  <div :class="['flex w-full mb-5', isUser ? 'justify-end' : 'justify-start']">
    
    <!-- Message Content Area -->
    <div :class="['max-w-[85%] sm:max-w-[80%] group relative', isUser ? 'flex flex-col items-end' : 'flex flex-col items-start']">
      
      <!-- Mode Tag Badge for AI -->
      <div v-if="!isUser && (Boolean(textContent && textContent.trim()) || hasSpecializedCard)" class="flex flex-wrap items-center gap-1.5 mb-1 px-1 text-[11px]">
        <span class="font-bold text-zinc-900 dark:text-zinc-100">AngkorVers AI</span>
        <span class="text-zinc-400">•</span>
        <span
          v-if="mode === 'offline' || mode === 'degraded' || mode === 'fallback'"
          class="inline-flex items-center gap-1 font-medium px-2 py-0.5 rounded-full bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-zinc-700 text-[10px]"
        >
          <WifiOff :size="9" /> Offline
        </span>
        <span
          v-else
          class="inline-flex items-center gap-1 font-medium px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border border-emerald-200/80 dark:border-emerald-800/60 text-[10px]"
        >
          <Wifi :size="9" /> Online
        </span>
      </div>

      <!-- Message Bubble Container -->
      <div
        v-if="isUser || (Boolean(textContent && textContent.trim()) || hasSpecializedCard)"
        :class="[
          'px-4 py-3 rounded-2xl text-[14.5px] sm:text-[15px]',
          hasKhmer ? 'leading-[1.75]' : 'leading-relaxed',
          isUser
            ? 'bg-zinc-800 dark:bg-zinc-700 text-white rounded-2xl font-normal sm:font-medium shadow-xs'
            : 'bg-white dark:bg-[#18181b] text-zinc-900 dark:text-zinc-100 border border-zinc-200/80 dark:border-zinc-800 rounded-2xl rounded-tl-xs w-full shadow-2xs'
        ]"
      >
        <!-- User Attached Files/Images Preview -->
        <div v-if="isUser && message.attachments && message.attachments.length > 0" class="mb-2 flex flex-wrap gap-1.5">
          <div
            v-for="(att, i) in message.attachments"
            :key="i"
            class="flex items-center space-x-1 bg-white/15 px-2 py-0.5 rounded-md text-xs text-white"
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
              class="px-3 py-1 text-xs rounded-full font-medium bg-white text-zinc-900 hover:bg-zinc-100 disabled:opacity-50 transition-colors cursor-pointer shadow-xs"
            >
              {{ isKhmer ? 'ផ្ញើ' : 'Send' }}
            </button>
          </div>
        </div>

        <!-- User Plain Text View -->
        <div v-else-if="isUser" class="whitespace-pre-wrap break-words leading-relaxed">
          {{ textContent }}
        </div>

        <!-- AI Rich Markdown Response View -->
        <div v-else class="message-text">
          <MarkdownRenderer :content="textContent" :is-khmer="hasKhmer" />
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
              <div v-if="src.google_maps_url || (src.website_links && src.website_links.length) || (src.picture_links && src.picture_links.length)" class="mt-1 pt-1 border-t border-slate-200/60 dark:border-zinc-800 flex flex-wrap items-center justify-end gap-2">
                <!-- Website Links (Link Only) -->
                <template v-if="src.website_links && src.website_links.length">
                  <a
                    v-for="(wlink, widx) in src.website_links.slice(0, 1)"
                    :key="'web-'+widx"
                    :href="wlink.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex items-center gap-0.5 text-[9px] font-bold text-emerald-600 dark:text-emerald-400 hover:underline"
                    :title="wlink.title"
                  >
                    <span>{{ isKhmer ? 'គេហទំព័រ' : 'Website' }}</span>
                    <ExternalLink :size="8" />
                  </a>
                </template>

                <!-- Picture Links (Link Only) -->
                <template v-if="src.picture_links && src.picture_links.length">
                  <a
                    v-for="(plink, pidx) in src.picture_links.slice(0, 1)"
                    :key="'pic-'+pidx"
                    :href="plink.image_url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex items-center gap-0.5 text-[9px] font-bold text-amber-600 dark:text-amber-400 hover:underline"
                    :title="plink.caption"
                  >
                    <ImageIcon :size="9" />
                    <span>{{ isKhmer ? 'រូបភាព' : 'Photo' }}</span>
                    <ExternalLink :size="8" />
                  </a>
                </template>

                <!-- Google Maps Link -->
                <a
                  v-if="src.google_maps_url"
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

        <!-- Contextual Suggested Topics Grid (Dynamic & Context-Aware) -->
        <div
          v-if="!isUser && isLatest && currentSuggestions && currentSuggestions.length > 0"
          class="mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800/80 w-full"
        >
          <div class="flex items-center justify-between mb-2 px-1">
            <span class="text-[11px] font-semibold text-slate-400 dark:text-zinc-500 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles :size="12" class="text-amber-500" />
              <span>{{ displayTopicTitle }}</span>
            </span>
            <button
              type="button"
              @click.stop="refreshSuggestions"
              :disabled="isRefreshingSuggestions"
              class="inline-flex items-center gap-1.5 text-[11px] font-medium text-slate-500 dark:text-zinc-400 hover:text-[#003E83] dark:hover:text-blue-400 px-2 py-0.5 rounded-full hover:bg-slate-100 dark:hover:bg-zinc-800 transition-all cursor-pointer group active:scale-95 disabled:opacity-50"
              :title="isKhmer ? 'ប្តូរសំណួរថ្មី' : 'Refresh questions'"
            >
              <RotateCcw
                :size="11"
                :class="['transition-transform duration-500', isRefreshingSuggestions ? 'animate-spin text-[#003E83] dark:text-blue-400' : 'group-hover:-rotate-90']"
              />
              <span>{{ isKhmer ? (isRefreshingSuggestions ? 'កំពុងផ្ទុក...' : 'ប្តូរសំណួរ') : (isRefreshingSuggestions ? 'Refreshing...' : 'Refresh') }}</span>
            </button>
          </div>

          <!-- Suggested Topic Cards Grid (2x2) -->
          <div :class="['grid grid-cols-1 sm:grid-cols-2 gap-2 transition-opacity duration-200', isRefreshingSuggestions ? 'opacity-50 pointer-events-none' : 'opacity-100']">
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
      <div v-if="!isUser && Boolean(textContent && textContent.trim())" class="flex items-center space-x-1 mt-1 text-slate-400 dark:text-slate-500">
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
  Landmark, Utensils, Calendar, Palmtree, Coins, Sun,
  Code, Calculator, Languages, Briefcase, Building2, GraduationCap
} from 'lucide-vue-next';
import ItineraryCard from './ItineraryCard.vue';
import WeatherCard from './WeatherCard.vue';
import RecommendationCard from './RecommendationCard.vue';
import CurrencyCard from '../cards/CurrencyCard.vue';
import MarkdownRenderer from './MarkdownRenderer.vue';
import { fetchChatSuggestions } from '../../services/chatService';

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

const enTopicsPool = [
  { id: 'angkor_wat', icon: markRaw(Landmark), title: 'Explore Angkor Wat & ancient temples', prompt: 'Tell me about the history, architecture, and sunrise spots at Angkor Wat.' },
  { id: 'itinerary', icon: markRaw(Calendar), title: '3-Day Siem Reap cultural itinerary', prompt: 'Create a 3-day Siem Reap cultural itinerary with top temples, costs, and tips.' },
  { id: 'phnom_penh', icon: markRaw(Landmark), title: 'Phnom Penh Royal Palace & riverfront', prompt: 'What are the top attractions and riverside experiences to explore in Phnom Penh?' },
  { id: 'islands', icon: markRaw(Palmtree), title: 'Koh Rong & tropical white-sand beaches', prompt: 'Tell me about speed ferries, resorts, and beaches on Koh Rong and Koh Rong Sanloem.' },
  { id: 'crab', icon: markRaw(Utensils), title: 'Fresh Kampot pepper crab in Kep', prompt: 'Tell me about fresh Kampot pepper crab in Kep and visiting Kep Crab Market.' },
  { id: 'nature', icon: markRaw(MapPin), title: 'Bokor National Park in Kampot', prompt: 'What can I explore at Bokor National Park and the historic hill station in Kampot?' },
  { id: 'battambang', icon: markRaw(Compass), title: 'Battambang Bamboo Train & bat caves', prompt: 'Tell me about the Bamboo Train, colonial architecture, and bat caves in Battambang.' },
  { id: 'mondulkiri', icon: markRaw(MapPin), title: 'Mondulkiri waterfalls & eco-tourism', prompt: 'What are the top eco-tourism spots, elephant sanctuaries, and waterfalls in Mondulkiri?' },
  { id: 'food', icon: markRaw(Utensils), title: 'Must-try authentic Khmer dishes & Amok', prompt: 'What authentic Khmer dishes like Fish Amok, Lok Lak, and Nom Banh Chok are must-try?' },
  { id: 'currency', icon: markRaw(Coins), title: 'Cambodia travel budget & USD vs Riel', prompt: 'What should I know about Cambodian currency, exchange rates, and tipping culture?' },
  { id: 'provinces', icon: markRaw(MapPin), title: '25 Provinces of Cambodia overview', prompt: 'Give an overview of the 25 administrative divisions of Cambodia with their top travel spots.' },
  { id: 'sunrise', icon: markRaw(Sun), title: 'Best time for Angkor Wat sunrise & weather', prompt: 'What is the best time and spot for Angkor Wat sunrise and best travel seasons?' }
];

const kmTopicsPool = [
  { id: 'angkor_wat', icon: markRaw(Landmark), title: 'ស្វែងយល់ពីប្រាសាទអង្គរវត្ត និងប្រវត្តិសាស្ត្រ', prompt: 'សូមរៀបរាប់អំពីប្រវត្តិសាស្ត្រ ស្ថាបត្យកម្ម និងកន្លែងមើលថ្ងៃរះស្អាតបំផុតនៅអង្គរវត្ត។' },
  { id: 'itinerary', icon: markRaw(Calendar), title: 'គម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប', prompt: 'រៀបចំគម្រោងដើរលេង ៣ ថ្ងៃនៅសៀមរាប រួមទាំងការស្នាក់នៅ ម្ហូបអាហារ និងកញ្ចប់ថវិកា។' },
  { id: 'phnom_penh', icon: markRaw(Landmark), title: 'ដើរលេងរាជធានីភ្នំពេញ និងព្រះបរមរាជវាំង', prompt: 'តើនៅភ្នំពេញមានកន្លែងកម្សាន្ត និងសារមន្ទីរប្រវត្តិសាស្ត្រណាខ្លះដែលគួរទៅទស្សនា?' },
  { id: 'islands', icon: markRaw(Palmtree), title: 'កោះរ៉ុង និងឆ្នេរខ្សាច់សកម្សាន្ត', prompt: 'ស្វែងយល់ពីដំណើរកម្សាន្តទៅកាន់កោះរ៉ុង និងកោះរ៉ុងសន្លឹម រួមទាំងអូប័រល្បឿនលឿន។' },
  { id: 'crab', icon: markRaw(Utensils), title: 'ក្តាមឆាម្រេចខ្ចីនៅកែប', prompt: 'តើក្តាមឆាម្រេចខ្ចីនៅកែប និងចម្ការម្រេចកំពតមានអ្វីពិសេស?' },
  { id: 'nature', icon: markRaw(MapPin), title: 'ឧទ្យានជាតិភ្នំបូកគោ ខេត្តកំពត', prompt: 'តើការឡើងកម្សាន្តលើភ្នំបូកគោមានតំបន់ទេសចរណ៍ និងសំណង់ប្រវត្តិសាស្ត្រណាខ្លះ?' },
  { id: 'battambang', icon: markRaw(Compass), title: 'ជិះឡូរីបាត់ដំបង និងទស្សនាល្អាងប្រចៀវ', prompt: 'សូមណែនាំដំណើរកម្សាន្តជិះឡូរី (Bamboo Train) និងមើលហ្វូងប្រចៀវនៅភ្នំសំពៅ បាត់ដំបង។' },
  { id: 'mondulkiri', icon: markRaw(MapPin), title: 'ទឹកធ្លាក់ប៊ូស្រា និងទេសចរណ៍មណ្ឌលគិរី', prompt: 'តើដំណើរកម្សាន្តទៅមណ្ឌលគិរី ទឹកធ្លាក់ប៊ូស្រា និងជម្រកដំរីមានអ្វីគួរចាប់អារម្មណ៍?' },
  { id: 'food', icon: markRaw(Utensils), title: 'ម្ហូបខ្មែរប្រពៃណី និងអាមុកត្រីមិនគួររំលង', prompt: 'តើម្ហូបខ្មែរប្រពៃណីណាខ្លះដែលមិនគួររំលង ដូចជាអាមុក ឡុកឡាក់ និងនំបញ្ចុក?' },
  { id: 'currency', icon: markRaw(Coins), title: 'ការចាយលុយដុល្លារ និងប្រាក់រៀល', prompt: 'តើការចាយលុយដុល្លារ និងប្រាក់រៀលនៅកម្ពុជាត្រូវដឹងអ្វីខ្លះ?' },
  { id: 'provinces', icon: markRaw(MapPin), title: 'រាជធានី-ខេត្តទាំង ២៥ នៃកម្ពុជា', prompt: 'សូមរៀបរាប់សង្ខេបអំពីរាជធានី-ខេត្តទាំង ២៥ នៅកម្ពុជា រួមទាំងសក្តានុពលទេសចរណ៍។' },
  { id: 'sunrise', icon: markRaw(Sun), title: 'ពេលវេលាល្អបំផុតមើលថ្ងៃរះអង្គរវត្ត', prompt: 'តើពេលវេលា និងទីតាំងណាដែលល្អបំផុតសម្រាប់ទស្សនាថ្ងៃរះនៅអង្គរវត្ត?' }
];

const displayTopicTitle = computed(() => {
  if (props.message.topic && props.message.topic.trim()) {
    return props.message.topic.trim();
  }
  return isKhmer.value ? 'ប្រធានបទណែនាំបន្ត' : 'Suggested Topics';
});

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
  } else if (s.includes('code') || s.includes('python') || s.includes('laravel') || s.includes('api') || s.includes('rag') || s.includes('vector') || s.includes('database') || s.includes('model') || s.includes('frontend') || s.includes('backend') || s.includes('កូដ') || s.includes('កម្មវិធី')) {
    icon = markRaw(Code);
  } else if (s.includes('math') || s.includes('gradient') || s.includes('calculus') || s.includes('algorithm') || s.includes('derivative') || s.includes('គណិត') || s.includes('ក្បួនដោះស្រាយ')) {
    icon = markRaw(Calculator);
  } else if (s.includes('business') || s.includes('startup') || s.includes('tax') || s.includes('gdt') || s.includes('camdx') || s.includes('register') || s.includes('moc') || s.includes('company') || s.includes('bakong') || s.includes('អាជីវកម្ម') || s.includes('ពន្ធ') || s.includes('ចុះបញ្ជី')) {
    icon = markRaw(Briefcase);
  } else if (s.includes('passport') || s.includes('visa') || s.includes('license') || s.includes('public service') || s.includes('ministry') || s.includes('gdi') || s.includes('mwt') || s.includes('លិខិតឆ្លងដែន') || s.includes('បើកបរ') || s.includes('សេវាសាធារណៈ') || s.includes('ក្រសួង')) {
    icon = markRaw(Building2);
  } else if (s.includes('school') || s.includes('university') || s.includes('bacii') || s.includes('education') || s.includes('scholarship') || s.includes('grade 12') || s.includes('សាលា') || s.includes('សាកលវិទ្យាល័យ') || s.includes('បាក់ឌុប') || s.includes('អាហារូបករណ៍') || s.includes('អប់រំ')) {
    icon = markRaw(GraduationCap);
  } else if (s.includes('translation') || s.includes('khmer language') || s.includes('orthography') || s.includes('chuon nath') || s.includes('dictionary') || s.includes('grammar') || s.includes('បកប្រែ') || s.includes('ភាសាខ្មែរ') || s.includes('អក្ខរាវិរុទ្ធ') || s.includes('វចនានុក្រម')) {
    icon = markRaw(Languages);
  } else if (s.includes('itinerary') || s.includes('day') || s.includes('festival') || s.includes('schedule') || s.includes('plan') || s.includes('គម្រោង') || s.includes('ថ្ងៃ') || s.includes('បុណ្យ') || s.includes('កាលវិភាគ')) {
    icon = markRaw(Calendar);
  } else if (s.includes('beach') || s.includes('island') || s.includes('koh rong') || s.includes('sea') || s.includes('resort') || s.includes('កោះ') || s.includes('ឆ្នេរ') || s.includes('សមុទ្រ')) {
    icon = markRaw(Palmtree);
  } else if (s.includes('currency') || s.includes('usd') || s.includes('riel') || s.includes('rate') || s.includes('cost') || s.includes('price') || s.includes('tip') || s.includes('budget') || s.includes('fee') || s.includes('ដុល្លារ') || s.includes('រៀល') || s.includes('តម្លៃ') || s.includes('ថ្លៃ') || s.includes('កម្រៃ')) {
    icon = markRaw(Coins);
  } else if (s.includes('sunrise') || s.includes('sunset') || s.includes('weather') || s.includes('season') || s.includes('sun') || s.includes('ថ្ងៃរះ') || s.includes('ថ្ងៃលិច') || s.includes('អាកាសធាតុ')) {
    icon = markRaw(Sun);
  } else if (s.includes('park') || s.includes('bokor') || s.includes('mountain') || s.includes('nature') || s.includes('place') || s.includes('spot') || s.includes('destination') || s.includes('province') || s.includes('tour') || s.includes('ឧទ្យាន') || s.includes('បូកគោ') || s.includes('ភ្នំ') || s.includes('ខេត្ត')) {
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
  const rawBackend = (props.message.suggestions || []).map(formatTopic).filter(Boolean);
  if (rawBackend.length >= 4 && excludeIds.length === 0) {
    return rawBackend.slice(0, 4);
  }

  const isKm = hasKhmer.value || isKhmer.value;
  const pool = isKm ? kmTopicsPool : enTopicsPool;

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

const refreshSuggestions = async () => {
  if (isRefreshingSuggestions.value) return;
  isRefreshingSuggestions.value = true;
  try {
    const currentList = currentSuggestions.value.map(c => c.prompt || c.title);
    const res = await fetchChatSuggestions({
      message: props.message.userQuery || textContent.value.slice(0, 120),
      answer: textContent.value,
      session_id: props.message.session_id,
      language: props.language,
      refresh: true,
      exclude: currentList,
      history: []
    });

    if (res && res.suggestions && res.suggestions.length > 0) {
      if (res.topic) {
        props.message.topic = res.topic;
      }
      currentSuggestions.value = res.suggestions.map(formatTopic).filter(Boolean);
      return;
    }
  } catch (err) {
    console.warn('Could not refresh suggestions via server API:', err);
  } finally {
    if (!currentSuggestions.value || currentSuggestions.value.length < 4) {
      const currentIds = currentSuggestions.value.map(c => c.id || c.title);
      currentSuggestions.value = getFreshSuggestions(currentIds);
    }
    setTimeout(() => {
      isRefreshingSuggestions.value = false;
    }, 300);
  }
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
