<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
}>();
</script>

<template>
  <div class="space-y-4">
    <WishlistCardInfo v-if="wishlistData" :wishlistData="wishlistData">
      <template #actions>
        <slot name="actions" />
      </template>
    </WishlistCardInfo>

    <WishlistItemCard
      v-if="wishlistData"
      v-for="item in wishlistData.items"
      :key="item.uuid"
      :wishlistItem="item"
    />

    <div v-else>Wishlist not found</div>
  </div>
</template>
