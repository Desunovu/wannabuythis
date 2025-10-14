<script setup lang="ts">
const { data: userData } = useAuth();
const route = useRoute();
const wishlistUuid = route.params.uuid as string;

const { data: wishlistData } = await useBackend("/wishlists/{uuid}", {
  path: {
    uuid: wishlistUuid,
  },
});

const isOwner = computed(() => {
  return wishlistData?.value?.owner_username === userData?.value?.username;
});
</script>

<template>
  <Wishlist :wishlistData="wishlistData" :isOwner="isOwner" />
</template>
