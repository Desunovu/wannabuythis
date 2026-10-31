<script setup lang="ts">
import type { components } from "#open-fetch-schemas/backend";
import WishlistActionButtonsModal from "./WishlistActionButtonsModal.vue";

const props = defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
  isOwner: boolean;
}>();

const { creationDateText, archivedText, itemsAmountText } = useWishlistInfo(
  props.wishlistData
);

const overlay = useOverlay();

const openWishlistActionsModal = (
  wishlist: components["schemas"]["WishlistResponse"]
) => {
  const modal = overlay.create(WishlistActionButtonsModal, {
    props: {
      wishlistUuid: props.wishlistData!.uuid,
      isArchived: props.wishlistData!.is_archived,
      isPublic: props.wishlistData!.is_public,
    },
  });
  modal.open();
};
</script>

<template>
  <div v-if="wishlistData" class="flex items-start justify-between py-4">
    <!-- Wishlist Info block -->
    <div>
      <div class="text-4xl font-bold text-neutral-100">
        {{ wishlistData.name }}
      </div>

      <div class="text-sm text-neutral-500">
        {{ itemsAmountText }}
      </div>

      <div class="text-sm text-neutral-500">
        {{ creationDateText }}
        {{ archivedText }}
      </div>
    </div>

    <div class="flex items-start gap-3">
      <UBadge
        v-if="wishlistData.is_public"
        color="green"
        variant="subtle"
        label="Public"
        class="self-start"
      />
      <UBadge
        v-else
        color="neutral"
        variant="subtle"
        label="Private"
        class="self-start"
      />

      <!-- Only show actions if the user is the owner -->
      <UButton
        v-if="isOwner"
        label="Edit wishlist"
        @click="openWishlistActionsModal(wishlistData)"
        class="self-start"
      />
    </div>
  </div>
</template>
