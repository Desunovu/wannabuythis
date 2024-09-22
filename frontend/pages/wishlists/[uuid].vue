<script setup lang="ts">
const { data: userData } = useAuth();
const route = useRoute();
const wishlistUuid = route.params.uuid as string;

const { data: wishlistData } = await useBackend("/wishlists/{uuid}", {
  path: {
    uuid: wishlistUuid,
  },
});
</script>

<template>
  <WishlistCard :wishlistData="wishlistData">
    <!-- If user is wishlist owner then show action buttons -->
    <template #actions>
      <WishlistActions
        v-if="userData?.username === wishlistData?.owner_username"
        :wishlistUuid="wishlistUuid"
        :isArchived="wishlistData?.is_archived"
      />
    </template>
  </WishlistCard>
</template>
