<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
import WishlistActionButtonsModal from "./WishlistActionButtonsModal.vue";

const props = defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
  isOwner: boolean;
}>();

const modal = useModal();

const openWishlistActionsModal = (
  wishlist: components["schemas"]["WishlistResponse"]
) => {
  modal.open(WishlistActionButtonsModal, {
    wishlistUuid: props.wishlistData!.uuid,
    isArchived: props.wishlistData!.is_archived,
  });
};
</script>

<template>
  <UCard v-if="wishlistData">
    <div class="flex items-center justify-between">
      <div class="basis-3/4 flex text-2xl">
        <img
          src="https://random.imagecdn.app/500/150"
          class="rounded-full w-24 h-24"
        />

        <div class="ml-4 flex items-center">
          {{ wishlistData.name }}
        </div>
      </div>

      <!-- Only show actions if the user is the owner -->
      <UButton
        v-if="isOwner"
        label="Edit wishlist"
        @click="openWishlistActionsModal(wishlistData)"
        class="self-start"
      />
    </div>
  </UCard>
</template>
