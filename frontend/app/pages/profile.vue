<script setup lang="ts">
const { data: userData } = useAuth();

const { data: wishlistsData } = await useBackend("/wishlists/");
</script>

<template>
  <Profile :userData="userData" :wishlistsData="wishlistsData">
    <template #right>
      <ProfileActionButtons />
    </template>
    
    <template #bottom>
      <WishlistPreviewArchivedGrid />
    </template>
  </Profile>
</template>
