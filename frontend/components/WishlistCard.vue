<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistData: components["schemas"]["WishlistResponse"] | null;
}>();
</script>

<template>
  <UCard v-if="wishlistData">
    <template #header>
      <div class="text-2xl">{{ wishlistData.name }}</div>
    </template>
      <div v-for="item in wishlistData.items" :key="item.uuid">
        <div>{{ item.name }}</div>
        <div>{{ item.quantity }} ({{ item.measurement_unit }})</div>
        <div>Importance: {{ item.priority }}</div>
        <div v-if="item.is_purchased">Purchased</div>
        <UDivider />
      </div>
  </UCard>
  <div v-else>Wishlist not found</div>
</template>
