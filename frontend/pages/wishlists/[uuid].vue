<script setup lang="ts">
const route = useRoute();
const wishlistUuid = route.params.uuid as string;

const { data: wishlistData } = await useBackend("/wishlists/{uuid}", {
  path: {
    uuid: wishlistUuid,
  },
});
</script>

<template>
  <WishlistCard :wishlistData="wishlistData" />
</template>