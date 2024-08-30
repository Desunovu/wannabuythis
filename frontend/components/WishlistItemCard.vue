<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistItem: components["schemas"]["WishlistItemResponse"];
}>();
</script>

<template>
  <UCard>
    <template #header>
      <div class="text-2xl">{{ wishlistItem.name }}</div>
    </template>
    <div>{{ wishlistItem.quantity }} ({{ wishlistItem.measurement_unit }})</div>
    <div>Importance: {{ wishlistItem.priority }}</div>
    <div v-if="wishlistItem.is_purchased">Purchased</div>
    <UDivider />
    <div class="flex justify-end space-x-2">
      <WishlistItemActions :wishlist-uuid="wishlistItem.wishlist_uuid" :wishlist-item-uuid="wishlistItem.uuid" :is-purchased="wishlistItem.is_purchased" />
    </div>
  </UCard>
</template>
