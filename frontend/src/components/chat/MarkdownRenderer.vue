<template>
  <div class="markdown-body space-y-2 text-zinc-900 dark:text-zinc-100 text-[14.5px] sm:text-[15px] leading-relaxed">
    <template v-for="(block, idx) in parsedBlocks" :key="idx">
      <!-- Fenced Code Block with Copy Button -->
      <CodeBlock
        v-if="block.type === 'code'"
        :code="block.rawCode"
        :lang="block.lang"
        :highlighted-html="block.html"
        :is-khmer="isKhmer"
      />

      <!-- Heading 1 -->
      <h1
        v-else-if="block.type === 'h1'"
        class="text-xl sm:text-2xl font-bold tracking-tight text-zinc-900 dark:text-white pt-2 pb-1 border-b border-zinc-200 dark:border-zinc-800"
        v-html="block.html"
      ></h1>

      <!-- Heading 2 -->
      <h2
        v-else-if="block.type === 'h2'"
        class="text-lg sm:text-xl font-bold text-zinc-900 dark:text-white pt-2 pb-0.5"
        v-html="block.html"
      ></h2>

      <!-- Heading 3 -->
      <h3
        v-else-if="block.type === 'h3'"
        class="text-base sm:text-lg font-semibold text-zinc-900 dark:text-zinc-100 pt-1"
        v-html="block.html"
      ></h3>

      <!-- Heading 4 -->
      <h4
        v-else-if="block.type === 'h4'"
        class="text-[15px] font-semibold text-zinc-800 dark:text-zinc-200"
        v-html="block.html"
      ></h4>

      <!-- Blockquote -->
      <blockquote
        v-else-if="block.type === 'blockquote'"
        class="pl-3.5 py-1 border-l-3 border-zinc-300 dark:border-zinc-700 text-zinc-600 dark:text-zinc-400 italic bg-zinc-50 dark:bg-zinc-800/40 rounded-r-md"
        v-html="block.html"
      ></blockquote>

      <!-- Unordered List Item -->
      <div
        v-else-if="block.type === 'ul_item'"
        class="flex items-start space-x-2 pl-1 leading-relaxed"
      >
        <span class="inline-block w-1.5 h-1.5 rounded-full bg-zinc-500 dark:bg-zinc-400 mt-2 shrink-0"></span>
        <span class="flex-1" v-html="block.html"></span>
      </div>

      <!-- Ordered List Item -->
      <div
        v-else-if="block.type === 'ol_item'"
        class="flex items-start space-x-2 pl-1 leading-relaxed"
      >
        <span class="font-semibold text-zinc-700 dark:text-zinc-300 text-xs mt-0.5 shrink-0 min-w-[16px]">
          {{ block.number }}.
        </span>
        <span class="flex-1" v-html="block.html"></span>
      </div>

      <!-- Table -->
      <div v-else-if="block.type === 'table'" class="my-2.5 overflow-x-auto rounded-lg border border-zinc-200 dark:border-zinc-800">
        <table class="min-w-full divide-y divide-zinc-200 dark:divide-zinc-800 text-xs sm:text-[13px]">
          <tbody class="divide-y divide-zinc-100 dark:divide-zinc-800/60">
            <tr
              v-for="(row, rIdx) in block.rows"
              :key="rIdx"
              :class="row.isHeader ? 'bg-zinc-100 dark:bg-zinc-800/80 font-semibold text-zinc-900 dark:text-white' : 'bg-white dark:bg-zinc-900/50 hover:bg-zinc-50 dark:hover:bg-zinc-800/30'"
            >
              <td
                v-for="(cell, cIdx) in row.cells"
                :key="cIdx"
                class="px-3 py-2 whitespace-normal"
                v-html="cell"
              ></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Horizontal Rule -->
      <hr v-else-if="block.type === 'hr'" class="my-3 border-zinc-200 dark:border-zinc-800" />

      <!-- Spacer -->
      <div v-else-if="block.type === 'spacer'" class="h-1"></div>

      <!-- Standard Paragraph -->
      <p
        v-else
        class="leading-relaxed"
        :class="{ 'font-khmer leading-[1.8]': isKhmer || /[\u1780-\u17FF]/.test(block.html) }"
        v-html="block.html"
      ></p>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { parseMarkdown } from '../../utils/markdownParser';
import CodeBlock from './CodeBlock.vue';

const props = defineProps({
  content: {
    type: String,
    required: true,
  },
  isKhmer: {
    type: Boolean,
    default: false,
  },
});

const parsedBlocks = computed(() => {
  return parseMarkdown(props.content);
});
</script>
