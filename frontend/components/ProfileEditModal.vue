<script setup lang="ts">
import ProfileChangeEmailModal from './ProfileChangeEmailModal.vue';
import ProfileChangePasswordModal from './ProfileChangePasswordModal.vue';

const modal = useModal();

const openChangeEmailModal = () => {
  modal.close();
  setTimeout(() => modal.open(ProfileChangeEmailModal), 400);
};

const openChangePasswordModal = () => {
  modal.close();
  setTimeout(() => modal.open(ProfileChangePasswordModal), 400);
};
</script>

<template>
  <UModal>
    <UCard>
      <div class="space-y-4">
        <UButton block @click="openChangeEmailModal"> Change email </UButton>
        <UButton block @click="openChangePasswordModal">
          Change password
        </UButton>
      </div>
    </UCard>
  </UModal>
</template>
