<script setup lang="ts">
import ItemCreateModal from "./ItemCreateModal.vue";
import WishlistChangeNameModal from "./WishlistChangeNameModal.vue";

const props = defineProps<{
  wishlistUuid: string;
  isArchived: boolean | undefined;
}>();

const modal = useModal();

const openWishlistChangeNameModal = async () => {
  modal.close();
  setTimeout(
    () =>
      modal.open(WishlistChangeNameModal, {
        wishlistUuid: props.wishlistUuid,
      }),
    400
  );
};
const openItemCreateModal = async () => {
  modal.close();
  setTimeout(
    () => modal.open(ItemCreateModal, { wishlistUuid: props.wishlistUuid }),
    400
  );
};
const archiveWishlist = async () => {
  await useBackend("/wishlists/archive/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
  });

  modal.close();
  reloadNuxtApp();
};
const unarchiveWishlist = async () => {
  await useBackend("/wishlists/unarchive/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
  });

  modal.close();
  reloadNuxtApp();
};
</script>

<template>
  <UModal>
    <UCard>
      <div class="text-2xl font-bold text-center mb-8">Wishlist actions</div>
      <div class="flex flex-col items-stretch space-y-4">
        <UButton class="justify-center" @click="openWishlistChangeNameModal">
          Change name
        </UButton>

        <UButton class="justify-center" @click="openItemCreateModal">
          Add item
        </UButton>

        <UButton
          v-if="!isArchived"
          class="justify-center"
          @click="archiveWishlist"
        >
          Archive
        </UButton>

        <UButton
          v-if="isArchived"
          class="justify-center"
          @click="unarchiveWishlist"
        >
          Unarchive
        </UButton>
      </div>
    </UCard>
  </UModal>
</template>
