<script setup lang="ts">
const newWishlistName = ref("");
const newEmail = ref("");
const oldPassword = ref("");
const newPassword = ref("");

const isCreatingWishlist = ref(false);
const isChangingEmail = ref(false);
const isChangingPassword = ref(false);

const createNewWishlist = async () => {
  await useBackend("/wishlists/create", {
    method: "POST",
    body: {
      wishlist_name: newWishlistName.value,
    },
  });
  newWishlistName.value = "";
  isCreatingWishlist.value = false;
  // TODO: handle error
  // TODO: handle success
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
    <UButton block @click="isCreatingWishlist = true">
      Create new wishlist
    </UButton>
    <UButton block @click="isChangingEmail = true"> Change email </UButton>
    <UButton block @click="isChangingPassword = true">
      Change password
    </UButton>
  </div>

  <UModal v-model="isCreatingWishlist">
    <UCard>
      <div class="space-y-4">
        <div>Creating new wishlist...</div>
      <UInput block v-model="newWishlistName" placeholder="New wishlist name" />
      <UButton block @click="createNewWishlist"> Create new wishlist </UButton>
      </div>
    </UCard>
  </UModal>

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
