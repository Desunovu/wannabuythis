<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";

const props = defineProps<{
  wishlistItem: components["schemas"]["WishlistItemResponse"];
}>();

const { priorityColor, priorityText, amountText } = useWishlistItemStyles(
  props.wishlistItem
);
</script>

<template>
  <UCard>
    <div class="flex flex-col items-center space-y-2 h-46">
      <UAvatar size="2xl" :text="wishlistItem.name.charAt(0)" />
      <div class="text-2xl font-bold">{{ wishlistItem.name }}</div>
      <div>{{ amountText }}</div>
      <div :class="priorityColor">{{ priorityText }}</div>
      <div v-if="wishlistItem.is_purchased" class="text-red-600 font-bold">
        Purchased
      </div>
    </div>
  </UCard>
</template>
