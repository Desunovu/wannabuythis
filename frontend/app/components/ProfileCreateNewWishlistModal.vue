<script setup lang="ts">
const overlay = useOverlay();

const newWishlistName = ref("");
const isPublic = ref(false);

const createNewWishlist = async () => {
  await useBackend("/wishlists/create", {
    method: "POST",
    body: {
      wishlist_name: newWishlistName.value,
      is_public: isPublic.value,
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
          <UCheckbox v-model="isPublic" label="Public wishlist" />
          <UButton block @click="createNewWishlist">
            Create new wishlist
          </UButton>
        </div>
      </UCard>
    </template>
  </UModal>
</template>
