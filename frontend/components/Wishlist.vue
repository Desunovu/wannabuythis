<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
import ItemModalCard from "./ItemModalCard.vue";

const modal = useModal();

const props = defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
  isOwner: boolean;
}>();

const openWishlistItemModal = (
  wishlistItem: components["schemas"]["WishlistItemResponse"]
) => {
  modal.open(ItemModalCard, {
    wishlistItem: wishlistItem,
    isOwner: props.isOwner,
  });
};
</script>

<template>
  <div class="space-y-4">
    <WishlistHeader
      v-if="wishlistData"
      :wishlistData="wishlistData"
      :isOwner="isOwner"
    />

    <div
      class="grid grid-cols-1 md:grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4"
      v-if="wishlistData"
    >
      <div
        v-for="item in wishlistData.items"
        :key="item.uuid"
        class="cursor-pointer"
        @click="openWishlistItemModal(item)"
      >
        <ItemCard :wishlistItem="item" />
      </div>
    </div>

    <div v-else>Wishlist not found</div>
  </div>
</template>
