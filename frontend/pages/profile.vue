<script setup lang="ts">
const { data: userData } = useAuth();
const username = ref(userData.value?.username ?? "");

const { data: wishlistsData } = await useBackend("/wishlists/user/{username}", {
  path: {
    username: username.value,
  },
});

const newEmail = ref("");
const oldPassword = ref("");
const newPassword = ref("");

const changeEmail = async () => {
  await useBackend("/users/me/email", {
    method: "PATCH",
    body: {
      new_email: newEmail.value,
    },
  });
};

const changePassword = async () => {
  await useBackend("/users/me/password", {
    method: "PATCH",
    body: {
      old_password: oldPassword.value,
      new_password: newPassword.value,
    },
  });
};

const createNewWishlist = async () => {
  await useBackend("/wishlists/create", {
    method: "POST",
    body: {
      wishlist_name: "New wishlist",
    },
  });
};
</script>

<template>
  <UserProfile :userData="userData" :wishlistsData="wishlistsData">
    <template #right>
      <UButton @click="createNewWishlist"> Create new wishlist </UButton>
      <div>
        <UInput v-model="newEmail" placeholder="New email" />
        <UButton @click="changeEmail"> Change email </UButton>
      </div>
      <div>
        <UInput v-model="oldPassword" placeholder="Old password" />
        <UInput v-model="newPassword" placeholder="New password" />
        <UButton @click="changePassword"> Change password </UButton>
      </div>
    </template>
  </UserProfile>
</template>
