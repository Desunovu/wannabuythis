<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";

const props = defineProps<{
  wishlist: components["schemas"]["WishlistResponse"];
}>();

const { creationDate } = useWishlistInfo(props.wishlist);
</script>

<template>
  <UCard>
    <div class="flex flex-col items-baseline space-x-2">
      <NuxtLink
        :to="`/wishlists/${wishlist.uuid}`"
        class="text-lg font-semibold"
      >
        {{ wishlist.name }}
      </NuxtLink>

      <div class="text-sm text-gray-500">
        {{ wishlist.items?.length }} items
      </div>

      <div class="text-sm text-gray-500">
        {{ creationDate }}
        {{ wishlist.is_archived ? "(archived)" : "" }}
      </div>
    </div>
  </UCard>
</template>
