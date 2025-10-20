<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
const { userData } = defineProps<{
  userData: components["schemas"]["PublicUserResponse"];
}>();

const initialLetter = computed(() => userData.username.charAt(0).toUpperCase());
</script>

<template>
  <div class="flex items-center space-x-4">
    <UAvatar size="2xl" :text="initialLetter" />
    <div>
      <div class="text-2xl">{{ userData.username }}</div>
    </div>
  </div>
</template>
