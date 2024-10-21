<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
import ItemModalCard from "./ItemModalCard.vue";

const props = defineProps<{
  items: components["schemas"]["WishlistItemResponse"][];
  isOwner: boolean;
}>();

const modal = useModal();

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
  <div
    class="grid grid-cols-1 md:grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4"
  >
    <ItemCard
      v-for="item in items"
      :key="item.uuid"
      :wishlistItem="item"
      class="cursor-pointer"
      @click="openWishlistItemModal(item)"
    />
  </div>
</template>
