<script setup lang="ts">
import ProfileChangeEmailModal from "./ProfileChangeEmailModal.vue";
import ProfileChangePasswordModal from "./ProfileChangePasswordModal.vue";

const overlay = useOverlay();

const openChangeEmailModal = () => {
  overlay.closeAll()
  const modal = overlay.create(ProfileChangeEmailModal);
  modal.open()
};

const openChangePasswordModal = () => {
  overlay.closeAll()
  const modal = overlay.create(ProfileChangePasswordModal);
  modal.open();
};
</script>

<template>
  <UModal>
    <template #content>
      <UCard>
        <div class="space-y-4">
          <UButton block @click="openChangeEmailModal"> Change email </UButton>
          <UButton block @click="openChangePasswordModal">
            Change password
          </UButton>
        </div>
      </UCard>
    </template>
  </UModal>
</template>
