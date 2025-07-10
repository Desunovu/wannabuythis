<script setup lang="ts">
const overlay = useOverlay();

const newWishlistName = ref("");

const createNewWishlist = async () => {
  await useBackend("/wishlists/create", {
    method: "POST",
    body: {
      wishlist_name: newWishlistName.value,
    },
  });

  newWishlistName.value = "";
  overlay.closeAll();
  reloadNuxtApp();
};
</script>

<template>
  <UModal>
    <template #content>
      <UCard>
        <div class="flex flex-col space-y-4">
          <div>Creating new wishlist...</div>
          <UInput
            block
            v-model="newWishlistName"
            placeholder="New wishlist name"
          />
          <UButton block @click="createNewWishlist">
            Create new wishlist
          </UButton>
        </div>
      </UCard>
    </template>
  </UModal>
</template>
