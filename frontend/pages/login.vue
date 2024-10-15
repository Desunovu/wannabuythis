<script setup lang="ts">
definePageMeta({
  auth: {
    unauthenticatedOnly: true,
    navigateAuthenticatedTo: "profile",
  }
})
</script>

<template>
  <div class="flex justify-end h-screen">
    <div class="flex justify-center items-center">
      <AuthLoginForm />
    </div>
  </div>
</template>
