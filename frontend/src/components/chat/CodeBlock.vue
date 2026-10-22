<template>
  <div class="my-3 rounded-xl overflow-hidden border border-zinc-200 dark:border-zinc-800 bg-[#0d1117] text-zinc-100 shadow-sm text-xs sm:text-[13px] font-mono group">
    <!-- Header bar with language & copy button -->
    <div class="flex items-center justify-between px-3.5 py-1.5 bg-[#161b22] border-b border-zinc-800 text-zinc-400 select-none">
      <div class="flex items-center space-x-2">
        <span class="flex space-x-1.5 mr-1">
          <span class="w-2.5 h-2.5 rounded-full bg-red-500/80"></span>
          <span class="w-2.5 h-2.5 rounded-full bg-amber-500/80"></span>
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-500/80"></span>
        </span>
        <span class="uppercase font-semibold tracking-wider text-[11px] text-zinc-300">
          {{ lang || 'code' }}
        </span>
      </div>

      <button
        type="button"
        @click="copyCode"
        class="inline-flex items-center gap-1.5 px-2 py-1 rounded-md text-[11px] font-medium text-zinc-300 hover:text-white bg-zinc-800/80 hover:bg-zinc-700/80 border border-zinc-700/60 transition-all cursor-pointer active:scale-95"
        :title="copied ? 'Copied to clipboard!' : 'Copy code'"
      >
        <Check v-if="copied" :size="12" class="text-emerald-400" />
        <Copy v-else :size="12" />
        <span>{{ copied ? (isKhmer ? 'បានចម្លង' : 'Copied!') : (isKhmer ? 'ចម្លង' : 'Copy code') }}</span>
      </button>
    </div>

    <!-- Code body -->
    <div class="p-3.5 overflow-x-auto leading-relaxed">
      <pre class="m-0"><code v-html="highlightedHtml"></code></pre>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { Copy, Check } from 'lucide-vue-next';

const props = defineProps({
  code: {
    type: String,
    required: true,
  },
  lang: {
    type: String,
    default: '',
  },
  highlightedHtml: {
    type: String,
    required: true,
  },
  isKhmer: {
    type: Boolean,
    default: false,
  },
});

const copied = ref(false);

const copyCode = async () => {
  try {
    if (navigator?.clipboard?.writeText) {
      await navigator.clipboard.writeText(props.code);
    } else {
      const el = document.createElement('textarea');
      el.value = props.code;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
    }
    copied.value = true;
    setTimeout(() => {
      copied.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy code:', err);
  }
};
</script>
