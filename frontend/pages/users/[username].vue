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
  }
})
</script>

<template>
  <div v-if="userData">
  <UserProfile v-if="userData" :userData="userData" />
  <WishlistsPreview v-if="wishlistsData" :wishlistsData="wishlistsData" />
  </div>
  <div v-else>User {{ username }} not found.</div>
</template>
