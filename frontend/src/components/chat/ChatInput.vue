<template>
  <div :class="['w-full', isCentered ? 'px-2 py-0' : 'bg-[#f8fafc] dark:bg-[#18181b] py-2 px-3 sm:px-4 sticky bottom-0 z-20']">
    <form @submit.prevent="handleSubmit" class="max-w-3xl mx-auto">
      
      <!-- Solid ChatGPT Pill-Shaped Input Box -->
      <div class="relative bg-white dark:bg-[#212121] border border-slate-300 dark:border-zinc-700 focus-within:border-slate-500 dark:focus-within:border-zinc-500 rounded-full px-3.5 py-1.5 sm:py-2 transition-colors">
        
        <!-- Attached Files/Images Preview Chips -->
        <div v-if="attachments.length > 0" class="flex flex-wrap gap-2 mb-2 px-1 pt-1">
          <div
            v-for="(att, idx) in attachments"
            :key="idx"
            class="flex items-center space-x-1.5 bg-slate-100 dark:bg-zinc-800 border border-slate-200 dark:border-zinc-700 px-2.5 py-1 rounded-full text-xs text-slate-800 dark:text-slate-200"
          >
            <ImageIcon :size="13" class="text-[#2563eb]" />
            <span class="truncate max-w-[120px] font-medium">{{ att.name }}</span>
            <button
              type="button"
              @click="removeAttachment(idx)"
              class="text-slate-400 hover:text-rose-500 p-0.5 rounded-full transition-colors cursor-pointer"
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
            accept="image/*,.pdf,.doc,.docx"
            class="hidden"
          />

          <!-- Plus / Attach Button -->
          <button
            type="button"
            @click="fileInputRef?.click()"
            :disabled="isLoading"
            class="w-8 h-8 rounded-full flex items-center justify-center text-slate-500 dark:text-zinc-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-zinc-800 transition-colors shrink-0 cursor-pointer"
            :title="isKhmer ? 'ភ្ជាប់ឯកសារ ឬរូបភាព' : 'Add attachment'"
          >
            <Plus :size="18" />
          </button>

          <!-- Main Textarea -->
          <textarea
            ref="textareaRef"
            rows="1"
            v-model="text"
            @input="adjustHeight"
            @keydown="handleKeyDown"
            :placeholder="isKhmer ? 'សួរអ្វីមួយអំពីកម្ពុជា...' : 'Ask something about Cambodia.'"
            :disabled="isLoading"
            :class="[
              'w-full bg-transparent text-[14px] sm:text-[15px] leading-relaxed text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-zinc-400 focus:outline-none resize-none px-1 py-1 max-h-32 min-h-[28px]',
              isKhmer || /[\u1780-\u17FF]/.test(text) ? 'font-khmer' : ''
            ]"
          ></textarea>

          <!-- Arrow-Up Send Button -->
          <button
            type="submit"
            :disabled="(!text.trim() && attachments.length === 0) || isLoading"
            :class="[
              'w-8 h-8 rounded-full bg-[#2563eb] hover:bg-[#1d4ed8] text-white flex items-center justify-center shrink-0 shadow-xs transition-all duration-150 active:scale-95',
              hasContent && !isLoading ? 'opacity-100 cursor-pointer' : 'opacity-40 cursor-not-allowed'
            ]"
            aria-label="Send message"
          >
            <ArrowUp :size="17" :stroke-width="2.5" />
          </button>

        </div>
      </div>

      <!-- Footer Disclaimer -->
      <p v-if="!isCentered" class="text-[11px] text-center text-slate-400 dark:text-zinc-500 mt-2">
        {{ isKhmer ? 'Angkor Verse AI ផ្តល់ព័ត៌មានផ្អែកលើទិន្នន័យទេសចរណ៍ផ្លូវការ' : 'Angkor Verse AI can make mistakes. Check important info.' }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue';
import { Plus, ArrowUp, X, Image as ImageIcon } from 'lucide-vue-next';

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

const emit = defineEmits(['send-message']);

const text = ref('');
const attachments = ref([]);
const textareaRef = ref(null);
const fileInputRef = ref(null);

const isKhmer = computed(() => props.language === 'km');
const hasContent = computed(() => Boolean(text.value.trim() || attachments.value.length > 0));

const adjustHeight = () => {
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto';
      textareaRef.value.style.height = `${Math.min(textareaRef.value.scrollHeight, 140)}px`;
    }
  });
};

watch(text, () => {
  adjustHeight();
});

const handleSubmit = () => {
  if ((!text.value.trim() && attachments.value.length === 0) || props.isLoading) return;
  emit('send-message', text.value.trim(), attachments.value);
  text.value = '';
  attachments.value = [];
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto';
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
  const files = Array.from(e.target.files || []);
  if (files.length === 0) return;

  const filePreviews = files.map((file) => ({
    name: file.name,
    size: (file.size / 1024).toFixed(1) + ' KB',
    type: file.type,
    url: URL.createObjectURL(file),
  }));

  attachments.value = [...attachments.value, ...filePreviews];
  e.target.value = '';
};

const removeAttachment = (index) => {
  attachments.value = attachments.value.filter((_, i) => i !== index);
};
</script>
