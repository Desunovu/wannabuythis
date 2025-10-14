<script setup lang="ts">
const { data } = useAuth();

const loggedInMenuItems = [
  { name: "Profile", icon: "i-heroicons-user-circle", to: "/profile" },
  {
    name: "Users",
    icon: "i-heroicons-magnifying-glass",
    to: "/users",
  },
  {
    name: "Logout",
    icon: "i-heroicons-arrow-right-on-rectangle",
    to: "/logout",
  },
];

const loggedOutMenuItems = [
  { name: "Login", icon: "i-heroicons-user-circle", to: "/login" },
  { name: "Register", icon: "i-heroicons-user-circle", to: "/register" },
];

const menuItems = computed(() => {
  return data.value ? loggedInMenuItems : loggedOutMenuItems;
});
</script>

<template>
  <div class="flex items-center justify-between my-4">
    <NuxtLink to="/" class="basis-1/4 text-3xl font-bold">
      Wannabuythis
    </NuxtLink>
    <div class="flex basis-3/4 justify-end">
      <UButton
        v-for="item in menuItems"
        :key="item.name"
        variant="ghost"
        :icon="item.icon"
        :to="item.to"
        :label="item.name"
      />
    </div>
  </div>
</template>
