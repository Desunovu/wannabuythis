<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
}>();
</script>

<template>
  <UCard v-if="wishlistData">
    <template #header>
      <div class="flex items-center justify-between">
        <div class="basis-3/4 flex text-2xl">
          <img
            src="https://random.imagecdn.app/500/150"
            class="rounded-full w-24 h-24"
          />

          <div class="ml-4 flex items-center">
            {{ wishlistData.name }}
          </div>
        </div>

        <!-- Slot for right action buttons -->
        <slot name="actions" class="basis-1/4" />
      </div>
    </template>
  </UCard>
</template>
