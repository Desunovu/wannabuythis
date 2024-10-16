<script setup lang="ts">
definePageMeta({
  auth: {
    unauthenticatedOnly: true,
    navigateAuthenticatedTo: "profile",
  },
});
const { data } = useAuth();
</script>

<template>
  <Landing />
</template>
