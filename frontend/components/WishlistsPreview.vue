<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistsData: components["schemas"]["WishlistResponse"][];
}>();
</script>

<template>
  <h1 v-if="wishlistsData.length" class="text-2xl font-bold">Wishlists</h1>
  <div v-if="wishlistsData.length === 0">No wishlists found</div>

  <div v-if="!wishlistsData">No wishlists found</div>
  <UCard v-for="wishlist in wishlistsData" :key="wishlist.uuid">
    <div class="flex flex-col group items-baseline space-x-2">
      <NuxtLink
        :to="`/wishlists/${wishlist.uuid}`"
        class="text-lg font-semibold"
      >
        {{ wishlist.name }}
      </NuxtLink>

      <div class="hidden group-hover:block text-sm text-gray-500">
        {{ wishlist.items.length }} items
      </div>

      <div class="text-sm hidden group-hover:block text-gray-500">
        Created at {{ new Date(wishlist.created_at).toLocaleDateString() }}
        {{ wishlist.is_archived ? "(archived)" : "" }}
      </div>
    </div>
  </UCard>
</template>
