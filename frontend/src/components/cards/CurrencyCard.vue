<template>
  <div v-if="currency" class="mt-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-3 shadow-2xs w-full">
    <div class="flex items-center justify-between gap-2 mb-2">
      <div class="flex items-center space-x-1.5">
        <DollarSign :size="16" class="text-emerald-500" />
        <span class="font-bold text-xs text-slate-900 dark:text-white">
          {{ isKhmer ? 'អត្រាប្តូរប្រាក់' : 'Currency Exchange' }}
        </span>
      </div>
      <span v-if="currency.source" class="text-[10px] text-slate-400">
        {{ currency.source }}
      </span>
    </div>

    <!-- Conversion Display -->
    <div class="flex items-center justify-around py-2 px-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800">
      <div class="text-center">
        <span class="text-xs text-slate-500 block">USD</span>
        <span class="text-sm font-bold text-slate-900 dark:text-white">
          ${{ currency.amount_usd || 1 }}
        </span>
      </div>
      <span class="text-slate-400 font-bold text-xs">➔</span>
      <div class="text-center">
        <span class="text-xs text-slate-500 block">KHR</span>
        <span class="text-sm font-bold text-emerald-600 dark:text-emerald-400">
          {{ currency.amount_khr ? Number(currency.amount_khr).toLocaleString() : '4,100' }} ៛
        </span>
      </div>
    </div>

    <!-- Exchange Rate Note -->
    <div v-if="currency.rate || currency.exchange_rate" class="mt-2 text-[10px] text-center text-slate-400 dark:text-slate-500">
      1 USD = {{ (currency.rate || currency.exchange_rate || 4100).toLocaleString() }} KHR
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { DollarSign } from 'lucide-vue-next';

const props = defineProps({
  currency: {
    type: Object,
    default: null,
  },
  language: {
    type: String,
    default: 'en',
  },
});

const isKhmer = computed(() => props.language === 'km');
</script>
