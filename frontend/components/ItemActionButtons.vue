<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
const props = defineProps<{
  wishlistUuid: string;
  wishlistItemUuid: string;
  isPurchased: boolean;
}>();

const modal = useModal();

const removeItem = async () => {
  await useBackend("/wishlists/remove-item/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
    body: {
      item_uuid: props.wishlistItemUuid,
    },
  });

  modal.close();
  reloadNuxtApp();
};

async function markAsPurchased() {
  await useBackend("/wishlists/mark-item-as-purchased/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
    body: {
      item_uuid: props.wishlistItemUuid,
    },
  });

  modal.close();
  reloadNuxtApp();
}

async function markAsNotPurchased() {
  await useBackend("/wishlists/mark-item-as-not-purchased/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
    body: {
      item_uuid: props.wishlistItemUuid,
    },
  });

  modal.close();
  reloadNuxtApp();
}
</script>

<template>
  <div class="flex flex-col space-y-2">
    <UButton class="justify-center" @click="removeItem">Remove item</UButton>
    <UButton
      v-if="!props.isPurchased"
      class="justify-center"
      @click="markAsPurchased"
    >
      Mark as purchased
    </UButton>
    <UButton
      v-if="props.isPurchased"
      class="justify-center"
      @click="markAsNotPurchased"
    >
      Mark as not purchased
    </UButton>
  </div>
</template>
