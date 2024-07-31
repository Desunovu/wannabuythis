<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{ userData: components["schemas"]["UserResponse"] }>();
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center space-x-4">
        <UAvatar size="2xl" :text="userData.username.charAt(0).toUpperCase()" />
        <div>
          <div class="text-2xl">{{ userData.username }}</div>
          <div>Email: {{ userData.email }}</div>
          <div v-if="!userData.is_active" class="text-red-500">(Email not verified)</div>
        </div>
      </div>
    </template>

    <div>Wishlist links will be displayed here</div>
  </UCard>
</template>
