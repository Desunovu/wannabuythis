<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
const { userData } = defineProps<{
  userData: components["schemas"]["PublicUserResponse"] | components["schemas"]["UserResponse"];
}>();

const initialLetter = computed(() => userData.username.charAt(0).toUpperCase());
</script>

<template>
  <div class="flex items-center space-x-4">
    <UAvatar size="2xl" :text="initialLetter" />
    <div>
      <div class="text-2xl">{{ userData.username }}</div>
      <div v-if="userData.email" class="text-sm text-neutral-500">
        {{ userData.email }}
      </div>
      <div v-if="userData.is_active !== undefined && !userData.is_active" class="text-sm text-neutral-500">
        Inactive
      </div>
    </div>
  </div>
</template>
