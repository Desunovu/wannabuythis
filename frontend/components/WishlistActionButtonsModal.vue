<script setup lang="ts">
const props = defineProps<{
  wishlistUuid: string;
  isArchived: boolean | undefined;
}>();
const changeWishlistName = async () => {
  await useBackend("/wishlists/change-name/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
    body: {
      new_name: "New name",
    },
  });
  // TODO: handle error
  // TODO: handle success
};
const addItem = async () => {
  await useBackend("/wishlists/add-item/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
    body: {
      name: "New item",
      quantity: 1,
      measurement_unit: "piece",
      priority: 1,
    },
  });
  // TODO: handle error
  // TODO: handle success
};
const archiveWishlist = async () => {
  await useBackend("/wishlists/archive/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
  });
  // TODO: handle error
  // TODO: handle success
};
const unarchiveWishlist = async () => {
  await useBackend("/wishlists/unarchive/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
  });
  // TODO: handle error
  // TODO: handle success
};
</script>

<template>
  <UModal>
    <UCard>
      <div class="text-2xl font-bold text-center mb-8">Wishlist actions</div>
      <div class="flex flex-col items-stretch space-y-4">
        <UButton class="justify-center" @click="changeWishlistName">
          Change name
        </UButton>

        <UButton class="justify-center" @click="addItem"> Add item </UButton>

        <UButton v-if="!isArchived" class="justify-center" @click="archiveWishlist">
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
