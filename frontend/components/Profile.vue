<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  userData: components["schemas"]["UserResponse"] | null;
  wishlistsData: components["schemas"]["WishlistResponse"][] | null;
}>();
</script>

<template>
  <UCard>
    <div class="flex items-start justify-between my-4">
      <ProfileInfo v-if="userData" :userData="userData" class="basis-3/4" />
      <slot name="right" class="basis-1/4" />
    </div>
    <div class="flex flex-col space-y-4 mt-4">
      <h1 class="text-2xl font-bold">Wishlists</h1>
      <WishlistsPreview v-if="wishlistsData" :wishlistsData="wishlistsData" />
      <slot name="bottom" />
    </div>
  </UCard>
</template>
