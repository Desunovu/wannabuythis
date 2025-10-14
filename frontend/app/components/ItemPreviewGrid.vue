<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
import ItemModalCard from "./ItemModalCard.vue";

const props = defineProps<{
  items: components["schemas"]["WishlistItemResponse"][];
  isOwner: boolean;
}>();

const overlay = useOverlay();

const openWishlistItemModal = (
  wishlistItem: components["schemas"]["WishlistItemResponse"],
) => {
  const modal = overlay.create(ItemModalCard, {
    props: {
      wishlistItem: wishlistItem,
      isOwner: props.isOwner,
    },
  });
  modal.open()
};
</script>

<template>
  <div
    class="grid grid-cols-1 gap-4 md:grid-cols-[repeat(auto-fit,minmax(250px,1fr))]"
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
