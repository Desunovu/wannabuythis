<script setup lang="ts">
const modal = useModal();

const newWishlistName = ref("");

const createNewWishlist = async () => {
  await useBackend("/wishlists/create", {
    method: "POST",
    body: {
      wishlist_name: newWishlistName.value,
    },
  });

  newWishlistName.value = "";
  modal.close();
  reloadNuxtApp();
};
</script>

<template>
  <UModal>
    <UCard>
      <div class="space-y-4">
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
  </UModal>
</template>
