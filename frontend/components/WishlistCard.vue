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

    <div
      class="grid grid-cols-1 md:grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4"
      v-if="wishlistData"
    >
      <WishlistItemCard
        v-for="item in wishlistData.items"
        :key="item.uuid"
        :wishlistItem="item"
        :isOwner="isOwner"
      />
    </div>

    <div v-else>Wishlist not found</div>
  </div>
</template>
