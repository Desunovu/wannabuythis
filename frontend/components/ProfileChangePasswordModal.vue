<script setup lang="ts">
const modal = useModal();

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
  modal.close();
  // TODO: handle error
  // TODO: handle success
};
</script>

<template>
  <UModal>
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