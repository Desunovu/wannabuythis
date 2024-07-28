<script setup lang="ts">
const { data } = useAuth();
</script>

<template>
  <UserProfile v-if="data" :userData="data" />
</template>
