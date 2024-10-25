<script setup lang="ts">
definePageMeta({
  auth: false,
});

const { data: userData } = await useBackend("/users/", {});
</script>

<template>
  <!-- <div v-if="data">
    <div v-for="user in data" :key="user.username">
      <NuxtLink :to="`/users/${user.username}`">{{ user.username }}</NuxtLink>
    </div>
  </div>
  <div v-else>No users found.</div> -->
  <UserPreviewGrid :users="userData" />
  <div v-if="userData?.length === 0">No users found.</div>
</template>
