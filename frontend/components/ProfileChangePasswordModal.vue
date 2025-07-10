<script setup lang="ts">
const overlay = useOverlay();

const oldPassword = ref("");
const newPassword = ref("");

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
  overlay.closeAll();
  reloadNuxtApp();
};
</script>

<template>
  <UModal>
    <template #content>
      <UCard>
        <div class="flex flex-col space-y-4">
          <div>Changing password...</div>
          <UInput block v-model="oldPassword" placeholder="Old password" />
          <UInput block v-model="newPassword" placeholder="New password" />
          <UButton block @click="changePassword">Change password</UButton>
        </div>
      </UCard>
    </template>
  </UModal>
</template>
