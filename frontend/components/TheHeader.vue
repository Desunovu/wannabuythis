<script setup lang="ts">
const { data } = useAuth();

const loggedInMenuItems = [
  { name: "Профиль", icon: "i-heroicons-user-circle", to: "/profile" },
  { name: "Поиск пользователя", icon: "i-heroicons-magnifying-glass", to: "/users" },
  { name: "Выйти", icon: "i-heroicons-arrow-right-on-rectangle", to: "/logout" },
];
const loggedOutMenuItems = [
  { name: "Войти", icon: "i-heroicons-user-circle", to: "/login" },
  { name: "Регистрация", icon: "i-heroicons-user-circle", to: "/register" },
];
const menuItems = ref(loggedOutMenuItems);

watch(data, () => {
  menuItems.value = data.value ? loggedInMenuItems : loggedOutMenuItems;
});

</script>

<template>
  <div class="flex items-center justify-between my-4">
    <NuxtLink to="/" class="basis-1/4 text-3xl font-bold">
      Wannabuythis
    </NuxtLink>
    <div class="flex basis-3/4 justify-end">
      <UButtonGroup>
        <UButton
          v-for="item in menuItems"
          :key="item.name"
          variant="ghost"
          :icon="item.icon"
          :to="item.to"
          :label="item.name"
        />
      </UButtonGroup>
    </div>
  </div>
</template>

