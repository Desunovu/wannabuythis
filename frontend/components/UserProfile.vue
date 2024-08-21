<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  userData: components["schemas"]["UserResponse"] | null;
  wishlistsData: components["schemas"]["WishlistResponse"][] | null;
}>();
</script>

<template>
  <UserProfileInfo v-if="userData" :userData="userData" />
  <WishlistsPreview v-if="wishlistsData" :wishlistsData="wishlistsData" />
</template>
