<script setup lang="ts">
const wishlistsArchivedData = ref();

const getArchivedWishlists = async () => {
  const response = await useBackend("/wishlists/archived", {
    method: "GET",
  });
  wishlistsArchivedData.value = response.data;
  console.log(wishlistsArchivedData.value);
};
</script>

<template>
  <div v-if="!wishlistsArchivedData">
    <UButton @click="getArchivedWishlists"> Show archived wishlists </UButton>
  </div>

  <h1 v-if="wishlistsArchivedData?.value.length" class="text-2xl font-bold">
    Archived Wishlists
  </h1>
  <div v-if="wishlistsArchivedData?.value.length === 0">
    No archived wishlists found
  </div>

  <WishlistPreviewCard
    v-for="wishlist in wishlistsArchivedData?.value"
    :key="wishlist.uuid"
    :wishlist="wishlist"
  />
</template>
