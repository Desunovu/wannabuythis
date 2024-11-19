<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";

const props = defineProps<{
  wishlist: components["schemas"]["WishlistResponse"];
}>();

const { creationDateText, archivedText, itemsAmountText } = useWishlistInfo(
  props.wishlist
);
</script>

<template>
  <UCard>
    <div class="flex flex-row justify-between items-center">
      <div class="flex flex-col items-baseline space-x-2">
        <NuxtLink
          :to="`/wishlists/${wishlist.uuid}`"
          class="text-lg font-semibold"
        >
          {{ wishlist.name }}
        </NuxtLink>

        <div class="text-sm text-gray-500">
          {{ itemsAmountText }}
        </div>

        <div class="text-sm text-gray-500">
          {{ creationDateText }}
          {{ archivedText }}
        </div>
      </div>

      <!-- Few items preview -->
      <div class="flex flex-row -space-x-2 overflow-x-auto">
        <UAvatar
          v-for="item in wishlist.items.slice(0, 3)"
          :key="item.uuid"
          size="2xl"
          :text="item.name.slice(0, 5)"
          class="h-12 w-12 rounded-full bg-gray-300 border border-gray-400 shadow-sm text-xs"
        />
        <div
          v-if="wishlist.items.length > 3"
          class="flex items-center justify-center w-12 h-12 border border-gray-400 rounded-full bg-gray-300 text-gray-500 text-2xl"
        >
          ...
        </div>
      </div>
    </div>
  </UCard>
</template>
