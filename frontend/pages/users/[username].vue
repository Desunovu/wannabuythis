<script setup lang="ts">
definePageMeta({
  auth: false,
});

const route = useRoute();
const username = route.params.username as string;

const { data: userData } = await useBackend("/users/{username}", {
  path: {
    username: username,
  },
});

const { data: wishlistsData } = await useBackend("/wishlists/user/{username}", {
  path: {
    username: username,
  },
});
</script>

<template>
  <Profile :userData="userData" :wishlistsData="wishlistsData" />
</template>
