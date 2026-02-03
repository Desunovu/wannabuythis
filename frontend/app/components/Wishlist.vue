<script setup lang="ts">
import type { components } from "#open-fetch-schemas/backend";

const props = defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
  isOwner: boolean;
}>();
</script>

<template>
  <div v-if="wishlistData" class="space-y-4">
    <WishlistHeader :wishlistData="wishlistData" :isOwner="isOwner" />

    <ItemPreviewGrid :items="wishlistData.items" :isOwner="isOwner" />
  </div>
  <div v-else>Wishlist not found</div>
</template>
