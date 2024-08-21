<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistsData: components["schemas"]["WishlistResponse"][] | null;
}>();
</script>

<template>
  <UCard v-for="wishlist in wishlistsData" :key="wishlist.uuid">
    <NuxtLink :to="`/wishlists/${wishlist.uuid}`">
      {{ wishlist.name }}
    </NuxtLink>
  </UCard>
</template>
