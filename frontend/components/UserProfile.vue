<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  userData: components["schemas"]["UserResponse"] | null;
  wishlistsData: components["schemas"]["WishlistResponse"][] | null;
}>();
</script>

<template>
  <div class="flex">
    <div class="flex-auto">
      <UserProfileInfo v-if="userData" :userData="userData" />
    </div>
    <div class="flex-shrink-0">
      <slot name="right" />
    </div>
  </div>
  <WishlistsPreview v-if="wishlistsData" :wishlistsData="wishlistsData" />
  <div class="mt-8">
    <slot name="bottom" />
  </div>
</template>
