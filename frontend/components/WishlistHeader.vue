<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
import WishlistActionButtonsModal from "./WishlistActionButtonsModal.vue";

const props = defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
  isOwner: boolean;
}>();

const { creationDateText, archivedText, itemsAmountText } = useWishlistInfo(props.wishlistData)

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
  <div v-if="wishlistData" class="flex items-start justify-between py-4">
    <!-- Wishlist Info block -->
    <div>
      <div class="text-4xl font-bold text-gray-100">
        {{ wishlistData.name }}
      </div>

      <div class="text-sm text-gray-500">
        {{ itemsAmountText }}
      </div>

      <div class="text-sm text-gray-500">
        {{ creationDateText }}
        {{ archivedText }}
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
</template>
