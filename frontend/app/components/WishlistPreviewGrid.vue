<script setup lang="ts">
import type { components } from "#open-fetch-schemas/backend";
defineProps<{
  wishlistsData: components["schemas"]["WishlistResponse"][];
}>();
</script>

<template>
  <h1 v-if="wishlistsData.length" class="text-2xl font-bold">Wishlists</h1>
  <div v-else>No wishlists found</div>

  <WishlistPreviewCard
    v-for="wishlist in wishlistsData"
    :key="wishlist.uuid"
    :wishlist="wishlist"
  />
</template>
