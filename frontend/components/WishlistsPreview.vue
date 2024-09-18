<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
defineProps<{
  wishlistsData: components["schemas"]["WishlistResponse"][] | null;
}>();
</script>

<template>
  <UCard v-for="wishlist in wishlistsData" :key="wishlist.uuid">
    <div class="flex flex-row items-center space-x-4">
      <div>
        <img
          src="https://random.imagecdn.app/500/150"
          class="rounded-full w-16 h-16"
          alt=""
        />
      </div>

      <div class="flex flex-col items-baseline space-x-2">
        <NuxtLink
          :to="`/wishlists/${wishlist.uuid}`"
          class="text-lg font-semibold"
        >
          {{ wishlist.name }}
        </NuxtLink>

        <div class="text-sm text-gray-500">
          {{ wishlist.items.length }} items
        </div>

        <div class="text-sm text-gray-500">
          Created at {{ new Date(wishlist.created_at).toLocaleDateString() }}
          {{ wishlist.is_archived ? "(archived)" : "" }}
        </div>


      </div>
    </div>
  </UCard>
</template>
