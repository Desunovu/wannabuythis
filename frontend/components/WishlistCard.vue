<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
}>();
</script>

<template>
  <UCard v-if="wishlistData">
    <template #header>
      <div class="text-2xl">{{ wishlistData.name }}</div>
    </template>
      <WishlistItemCard v-for="item in wishlistData.items" :key="item.uuid" :wishlistItem="item" />
  </UCard>
  <div v-else>Wishlist not found</div>
</template>
