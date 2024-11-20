<script setup lang="ts">
const modal = useModal();

const newEmail = ref("");

const changeEmail = async () => {
  await useBackend("/users/me/email", {
    method: "PATCH",
    body: {
      new_email: newEmail.value,
    },
  });

  newEmail.value = "";
  modal.close();
  reloadNuxtApp();
};
</script>

<template>
  <UModal>
    <UCard>
      <div class="space-y-4">
        <div>Changing email...</div>
        <UInput block v-model="newEmail" placeholder="New email" />
        <UButton block @click="changeEmail"> Change email </UButton>
      </div>
    </UCard>
  </UModal>
</template>
