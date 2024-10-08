<script setup lang="ts">
import ProfileCreateNewWishlistModal from "./ProfileCreateNewWishlistModal.vue";
import ProfileEditModal from "./ProfileEditModal.vue";

const modal = useModal();

const openCreateNewWishlistModal = () => {
  modal.open(ProfileCreateNewWishlistModal);
};

const openProfileEditModal = () => {
  modal.open(ProfileEditModal);
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
