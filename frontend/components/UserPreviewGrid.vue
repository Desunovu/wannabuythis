<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";

const props = defineProps<{
  users: components["schemas"]["UserResponse"][];
}>();
</script>

<template>
  <div
    class="grid grid-cols-1 md:grid-cols-3 gap-4"
  >
    <UserPreviewCard
      v-for="user in users"
      :user="user"
      :key="user.username"
      @click="navigateTo(`/users/${user.username}`)"
    />
  </div>
</template>
