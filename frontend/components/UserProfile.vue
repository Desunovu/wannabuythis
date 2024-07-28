<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{ userData: components["schemas"]["UserResponse"] }>();
</script>

<template>
  <div>{{ userData.username }}'s Profile</div>
</template>
