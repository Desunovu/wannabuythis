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

  <div v-if="wishlistsArchivedData?.value.length > 0">
    <div>Archived wishlists:</div>
    <WishlistsPreview :wishlistsData="wishlistsArchivedData.value" />
  </div>
  
  <div v-if="wishlistsArchivedData?.value.length === 0">
    No archived wishlists found
  </div>
</template>
