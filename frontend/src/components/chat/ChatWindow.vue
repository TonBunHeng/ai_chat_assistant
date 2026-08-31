<template>
  <div ref="chatContainerRef" class="flex-1 overflow-y-auto px-3 py-4 sm:px-6 sm:py-8 bg-[#f8fafc] dark:bg-[#18181b] transition-colors duration-200">
    <div class="max-w-4xl mx-auto space-y-4">
      
      <!-- Active Chat Conversation Messages -->
      <ChatMessage
        v-for="(msg, index) in messages"
        :key="msg.id || index"
        :message="msg"
        :language="language"
        @regenerate="$emit('regenerate')"
        @select-suggestion="(s) => $emit('send-message', s)"
      />

      <!-- Loading / Typing Indicator -->
      <TypingIndicator v-if="isLoading" :language="language" />

      <!-- Error Alert Box -->
      <div
        v-if="error"
        class="my-4 p-4 rounded-2xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800/80 text-rose-800 dark:text-rose-300 text-sm flex items-start space-x-3 shadow-xs"
      >
        <AlertCircle :size="20" class="text-rose-500 shrink-0 mt-0.5" />
        <div class="flex-1">
          <p class="font-semibold">{{ isKhmer ? 'មានបញ្ហាក្នុងការតភ្ជាប់' : 'Connection Warning' }}</p>
          <p class="text-xs text-rose-600 dark:text-rose-400 mt-0.5">{{ error }}</p>
        </div>
      </div>

      <div ref="messagesEndRef"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue';
import { AlertCircle } from 'lucide-vue-next';
import ChatMessage from './ChatMessage.vue';
import TypingIndicator from './TypingIndicator.vue';

const props = defineProps({
  messages: {
    type: Array,
    default: () => [],
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  error: {
    type: String,
    default: null,
  },
  language: {
    type: String,
    default: 'en',
  },
});

defineEmits(['send-message', 'regenerate']);

const messagesEndRef = ref(null);
const chatContainerRef = ref(null);
const isKhmer = computed(() => props.language === 'km');

const scrollToBottom = () => {
  nextTick(() => {
    messagesEndRef.value?.scrollIntoView({ behavior: 'smooth' });
  });
};

watch(
  () => [props.messages.length, props.isLoading],
  () => {
    scrollToBottom();
  }
);

onMounted(() => {
  scrollToBottom();
});
</script>
