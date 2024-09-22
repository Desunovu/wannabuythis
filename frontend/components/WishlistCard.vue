<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
  isOwner: boolean;
}>();
</script>

<template>
  <div class="space-y-4">
    <WishlistCardInfo
      v-if="wishlistData"
      :wishlistData="wishlistData"
      :isOwner="isOwner"
    />

    <WishlistItemCard
      v-if="wishlistData"
      v-for="item in wishlistData.items"
      :key="item.uuid"
      :wishlistItem="item"
      :isOwner="isOwner"
    />

    <div v-else>Wishlist not found</div>
  </div>
</template>
