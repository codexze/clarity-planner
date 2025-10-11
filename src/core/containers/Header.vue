<template>
  <header class="sticky top-0 z-10 bg-white shadow-sm">
    <div class="mx-8 max-w-7xl py-4 sm:px-6 lg:px-4">
      <div class="flex items-center justify-between gap-3 min-h-[3rem] sm:min-h-[4rem]">
        <!-- Back button for mobile (only shows if can go back) -->
        <button v-if="canGoBack" @click="goBack" class="inline-flex items-center justify-center p-2 -ml-2 text-gray-500 rounded-md hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 lg:hidden">
          <ChevronLeftIcon class="w-5 h-5" aria-hidden="true" />
          <span class="sr-only">Go back</span>
        </button>

        <!-- Title section with optional breadcrumb -->
        <div class="min-w-0 items-center">
          <span v-if="$route.meta.label" class="hidden truncate text-xl font-bold text-blue-500 sm:block">
            {{ $route.meta.label }}
          </span>
          <span class="truncate text-md font-semibold text-gray-900">
            {{ $route.meta.title }}
          </span>
          <p class="text-sm text-gray-600">{{ $route.meta.description }}</p>
        </div>

        <!-- Action buttons -->
        <div class="flex items-center gap-2">
          <slot name="actions"></slot>
        </div>
      </div>

      <!-- Mobile subtitle (if present) -->
      <div v-if="$route.meta.label" class="mt-1 truncate text-sm text-blue-500 sm:hidden">
        {{ $route.meta.label }}
      </div>
    </div>
  </header>
</template>

<script setup>
import { ChevronLeftIcon } from '@heroicons/vue/24/outline';
import { useRouter } from 'vue-router';
import { computed } from 'vue';

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: '',
  },
  showBackButton: {
    type: Boolean,
    default: false,
  },
});

const router = useRouter();
const canGoBack = computed(() => props.showBackButton && window.history.length > 1);

const goBack = () => {
  router.back();
};
</script>
