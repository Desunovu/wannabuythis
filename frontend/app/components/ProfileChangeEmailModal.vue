<script setup lang="ts">
const overlay = useOverlay();

const newEmail = ref("");

const changeEmail = async () => {
  await useBackend("/users/me/email", {
    method: "PATCH",
    body: {
      new_email: newEmail.value,
    },
  });

  newEmail.value = "";
  overlay.closeAll();
  reloadNuxtApp();
};
</script>

<template>
  <UModal>
    <template #content>
      <UCard>
        <div class="flex flex-col space-y-4">
          <div>Changing email...</div>
          <UInput block v-model="newEmail" placeholder="New email" />
          <UButton block @click="changeEmail">Change email</UButton>
        </div>
      </UCard>
    </template>
  </UModal>
</template>
