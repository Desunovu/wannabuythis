<script setup lang="ts">
definePageMeta({
  auth: false,
});

const route = useRoute();
const username = route.params.username as string;

const { data } = await useBackend("/users/{username}", {
  path: {
    username: username,
  },
});
</script>

<template>
  <div v-if="data">
    <UserProfile :userData="data" />
  </div>
  <div v-else>User {{ username }} not found.</div>
</template>
