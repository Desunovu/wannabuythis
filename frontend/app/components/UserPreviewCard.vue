<script setup lang="ts">
import type { components } from "#open-fetch-schemas/backend";

const props = defineProps<{
  user: components["schemas"]["UserResponse"];
}>();
</script>

<template>
  <UCard @click="navigateTo(`/users/${user.username}`)">
    <div class="flex flex-col items-center cursor-pointer space-y-4">
      <UAvatar size="2xl" :text="user.username.charAt(0)" class="rounded-lg" />
      <div class="text-2xl font-bold text-center">
        {{ user.username }}
      </div>
    </div>
  </UCard>
</template>
