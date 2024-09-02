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
  <div class="flex flex-col space-y-2">
    <UButton @click="changeWishlistName"> Change name </UButton>
    <UButton @click="addItem"> Add item </UButton>
    <UButton @click="archiveWishlist"> Archive </UButton>
    <UButton v-if="isArchived" @click="unarchiveWishlist"> Unarchive </UButton>
  </div>
</template>
