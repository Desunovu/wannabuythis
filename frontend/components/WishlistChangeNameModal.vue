<script setup lang="ts">
const props = defineProps<{
  wishlistUuid: string;
}>();

const modal = useModal();
const newWishlistName = ref("");

const changeWishlistName = async () => {
  await useBackend("/wishlists/change-name/{wishlist_uuid}", {
    method: "POST",
    path: {
      wishlist_uuid: props.wishlistUuid,
    },
    body: {
      new_name: newWishlistName.value,
    },
  });


  modal.close();
  reloadNuxtApp();
};
</script>

<template>
  <UModal>
    <UCard>
      <div class="space-y-4">
        <div>Changing wishlist name...</div>
        <UInput
          block
          v-model="newWishlistName"
          placeholder="New wishlist name"
        />
        <UButton block @click="changeWishlistName">
          Change wishlist name
        </UButton>
      </div>
    </UCard>
  </UModal>
</template>
