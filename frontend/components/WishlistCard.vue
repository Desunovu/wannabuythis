<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
  isOwner: boolean;
}>();
const isWishlistItemModalOpen = ref(false);
const modalWishlistItemData = ref<
  components["schemas"]["WishlistItemResponse"] | null
>(null);

const openWishlistItemModal = (
  wishlistItem: components["schemas"]["WishlistItemResponse"]
) => {
  modalWishlistItemData.value = wishlistItem;
  isWishlistItemModalOpen.value = true;
  console.log(
    "openWishlistItemModal",
    modalWishlistItemData.value,
    isWishlistItemModalOpen.value
  );
};
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
      <div
        v-for="item in wishlistData.items"
        :key="item.uuid"
        class="cursor-pointer"
        @click="openWishlistItemModal(item)"
      >
        <WishlistItemCard :wishlistItem="item" />
      </div>
    </div>

    <div v-else>Wishlist not found</div>
  </div>

  <UModal v-model="isWishlistItemModalOpen">
    <WishlistItemModalCard
      :wishlistItem="modalWishlistItemData"
      :isOwner="isOwner"
    />
  </UModal>
</template>
