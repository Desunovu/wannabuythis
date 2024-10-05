<script setup lang="ts">
const { data: userData } = useAuth();
const username = ref(userData.value?.username ?? "");

const { data: wishlistsData } = await useBackend("/wishlists/user/{username}", {
  path: {
    username: username.value,
  },
});

</script>

<template>
  <Profile :userData="userData" :wishlistsData="wishlistsData">
    <template #right>
      <ProfileActions />
    </template>
    <template #bottom>
      <WishlistsArchivedPreview />
    </template>
  </Profile>
</template>
