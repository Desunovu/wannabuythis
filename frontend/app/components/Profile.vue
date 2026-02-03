<script setup lang="ts">
import type { components } from "#open-fetch-schemas/backend";

defineProps<{
  userData: components["schemas"]["PublicUserResponse"] | components["schemas"]["UserResponse"] | null;
  wishlistsData: components["schemas"]["WishlistResponse"][] | null;
}>();
</script>

<template>
  <div class="flex items-start justify-between my-4">
    <ProfileInfo v-if="userData" :userData="userData" class="basis-3/4" />
    <slot name="right" class="basis-1/4" />
  </div>
  <div class="flex flex-col space-y-4 mt-4">
    <WishlistPreviewGrid v-if="wishlistsData" :wishlistsData="wishlistsData" />
    <slot name="bottom" />
  </div>
</template>
