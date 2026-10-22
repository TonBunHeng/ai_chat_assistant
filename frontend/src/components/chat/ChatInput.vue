<template>
  <div :class="['w-full', isCentered ? 'px-2 py-0' : 'bg-transparent py-2.5 px-3 sm:px-4 sticky bottom-0 z-20']">
    <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto">
      
      <!-- Modern Minimal ChatGPT-style Pill Input Box -->
      <div class="relative bg-white dark:bg-[#212121] border border-zinc-300/90 dark:border-zinc-700/80 hover:border-zinc-400 dark:hover:border-zinc-600 focus-within:border-zinc-600 dark:focus-within:border-zinc-400 focus-within:ring-2 focus-within:ring-zinc-400/20 dark:focus-within:ring-zinc-600/30 rounded-3xl px-3.5 py-1.5 sm:py-2 transition-all duration-200 shadow-xs">
        
        <!-- Attached Files/Images Preview Chips -->
        <div v-if="attachments.length > 0" class="flex flex-wrap gap-2 mb-2 px-1 pt-1">
          <div
            v-for="(att, idx) in attachments"
            :key="idx"
            class="flex items-center space-x-1.5 bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 px-2.5 py-1 rounded-full text-xs text-zinc-800 dark:text-zinc-200"
          >
            <ImageIcon :size="13" class="text-zinc-600 dark:text-zinc-400" />
            <span class="truncate max-w-[120px] font-medium">{{ att.name }}</span>
            <button
              type="button"
              @click="removeAttachment(idx)"
              class="text-zinc-400 hover:text-rose-500 p-0.5 rounded-full transition-colors cursor-pointer"
            >
              <X :size="12" />
            </button>
          </div>
        </div>

        <!-- Controls Row -->
        <div class="flex items-center space-x-1.5 sm:space-x-2">
          
          <!-- Hidden File Input -->
          <input
            type="file"
            ref="fileInputRef"
            @change="handleFileChange"
            multiple
            accept="image/*,.pdf,.doc,.docx,.txt,.md"
            class="hidden"
          />

          <!-- Plus / Attach Button -->
          <button
            type="button"
            @click="fileInputRef?.click()"
            :disabled="isLoading"
            class="w-8 h-8 rounded-full flex items-center justify-center text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-all duration-200 shrink-0 cursor-pointer active:scale-90 group"
            :title="isKhmer ? 'ភ្ជាប់ឯកសារ ឬរូបភាព' : 'Add attachment'"
          >
            <Plus :size="17" class="group-hover:scale-110 transition-transform duration-200" />
          </button>

          <!-- Main Textarea -->
          <textarea
            ref="textareaRef"
            rows="1"
            v-model="text"
            @input="adjustHeight"
            @keydown="handleKeyDown"
            :placeholder="isKhmer ? 'សួរអ្វីមួយអំពីកម្ពុជា ឬប្រធានបទណាមួយ...' : 'Message Cambodia Super AI...'"
            :disabled="isLoading"
            :class="[
              'w-full bg-transparent text-[14px] sm:text-[15px] leading-relaxed text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none resize-none px-1 py-1 max-h-36 min-h-[28px]',
              isKhmer || /[\u1780-\u17FF]/.test(text) ? 'font-khmer' : ''
            ]"
          ></textarea>

          <!-- Stop Generating Button when loading -->
          <button
            v-if="isLoading"
            type="button"
            @click="$emit('stop-generating')"
            class="w-8 h-8 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 flex items-center justify-center shrink-0 shadow-xs transition-all duration-200 active:scale-90 cursor-pointer"
            :title="isKhmer ? 'បញ្ឈប់ការបង្កើត' : 'Stop generating'"
            aria-label="Stop generating"
          >
            <Square :size="11" class="fill-current" />
          </button>

          <!-- Arrow-Up Send Button when not loading -->
          <button
            v-else
            type="submit"
            :disabled="!hasContent"
            :class="[
              'w-8 h-8 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 flex items-center justify-center shrink-0 shadow-xs transition-all duration-200 active:scale-90',
              hasContent ? 'opacity-100 cursor-pointer hover:shadow-md' : 'opacity-30 cursor-not-allowed'
            ]"
            aria-label="Send message"
          >
            <ArrowUp :size="16" :stroke-width="2.5" />
          </button>

        </div>
      </div>

      <!-- Footer Disclaimer -->
      <p v-if="!isCentered" class="text-[11px] text-center text-zinc-400 dark:text-zinc-500 mt-2 select-none">
        {{ isKhmer ? 'Cambodia Super AI អាចមានកំហុស។ សូមផ្ទៀងផ្ទាត់ព័ត៌មានសំខាន់ៗ។' : 'Cambodia Super AI can make mistakes. Verify important facts.' }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue';
import { Plus, ArrowUp, Square, X, Image as ImageIcon } from 'lucide-vue-next';

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false,
  },
  language: {
    type: String,
    default: 'en',
  },
  isCentered: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['send-message', 'stop-generating']);

const text = ref('');
const attachments = ref([]);
const textareaRef = ref(null);
const fileInputRef = ref(null);

const isKhmer = computed(() => props.language === 'km');
const hasContent = computed(() => text.value.trim().length > 0 || attachments.value.length > 0);

const adjustHeight = () => {
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto';
      const newHeight = Math.min(textareaRef.value.scrollHeight, 144);
      textareaRef.value.style.height = `${newHeight}px`;
    }
  });
};

const handleKeyDown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSubmit();
  }
};

const handleFileChange = (e) => {
  const files = e.target.files;
  if (!files || files.length === 0) return;

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const reader = new FileReader();
    reader.onload = (loadEvent) => {
      attachments.value.push({
        name: file.name,
        type: file.type,
        size: file.size,
        base64: loadEvent.target.result,
        data: loadEvent.target.result,
      });
    };
    reader.readAsDataURL(file);
  }
  if (fileInputRef.value) {
    fileInputRef.value.value = '';
  }
};

const removeAttachment = (idx) => {
  attachments.value.splice(idx, 1);
};

const handleSubmit = () => {
  if ((!text.value.trim() && attachments.value.length === 0) || props.isLoading) return;
  const currentMsg = text.value.trim();
  const currentAttachments = [...attachments.value];
  
  emit('send-message', currentMsg, currentAttachments);
  
  text.value = '';
  attachments.value = [];
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto';
    }
  });
};

watch(() => props.isLoading, (loading) => {
  if (!loading) {
    nextTick(() => {
      textareaRef.value?.focus();
    });
  }
});
</script>
