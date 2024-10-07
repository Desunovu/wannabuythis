<script setup lang="ts">
import ProfileCreateNewWishlistModal from "./ProfileCreateNewWishlistModal.vue";

const modal = useModal();

const newEmail = ref("");
const oldPassword = ref("");
const newPassword = ref("");

const isChangingEmail = ref(false);
const isChangingPassword = ref(false);

const openCreateNewWishlistModal = () => {
  modal.open(ProfileCreateNewWishlistModal);
};

const changeEmail = async () => {
  await useBackend("/users/me/email", {
    method: "PATCH",
    body: {
      new_email: newEmail.value,
    },
  });
  newEmail.value = "";
  isChangingEmail.value = false;
  // TODO: handle error
  // TODO: handle success
};

const changePassword = async () => {
  await useBackend("/users/me/password", {
    method: "PATCH",
    body: {
      old_password: oldPassword.value,
      new_password: newPassword.value,
    },
  });
  oldPassword.value = "";
  newPassword.value = "";
  isChangingPassword.value = false;
  // TODO: handle error
  // TODO: handle success
};
</script>

<template>
  <div class="flex flex-col space-y-4">
    <UButton block @click="openCreateNewWishlistModal">
      Create new wishlist
    </UButton>
    <UButton block @click="isChangingEmail = true"> Change email </UButton>
    <UButton block @click="isChangingPassword = true">
      Change password
    </UButton>
  </div>

  <UModal v-model="isChangingEmail">
    <UCard>
      <div class="space-y-4">
        <div>Changing email...</div>
        <UInput block v-model="newEmail" placeholder="New email" />
        <UButton block @click="changeEmail"> Change email </UButton>
      </div>
    </UCard>
  </UModal>

  <UModal v-model="isChangingPassword">
    <UCard>
      <div class="space-y-4">
        <div>Changing password...</div>
        <UInput block v-model="oldPassword" placeholder="Old password" />
        <UInput block v-model="newPassword" placeholder="New password" />
        <UButton block @click="changePassword"> Change password </UButton>
      </div>
    </UCard>
  </UModal>
</template>
