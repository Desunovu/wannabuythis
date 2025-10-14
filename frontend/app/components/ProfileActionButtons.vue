<script setup lang="ts">
import ProfileCreateNewWishlistModal from "./ProfileCreateNewWishlistModal.vue";
import ProfileEditModal from "./ProfileEditModal.vue";

const overlay = useOverlay();

const openCreateNewWishlistModal = () => {
  const modal = overlay.create(ProfileCreateNewWishlistModal);
  const instance = modal.open();
};

const openProfileEditModal = () => {
  const modal = overlay.create(ProfileEditModal);
  const instance = modal.open();
};
</script>

<template>
  <div class="flex flex-col space-y-4">
    <UButton block @click="openCreateNewWishlistModal">
      Create new wishlist
      </UButton>
    <UButton block @click="openProfileEditModal">
      Edit profile
    </UButton>
  </div>
</template>
