<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";

const userSearchQuery = ref("");
const users = ref<components["schemas"]["UserResponse"][] | null>(null);
const loading = ref(false);

const fetchUsers = async () => {
  loading.value = true;
  try {
    const { data } = await useBackend("/users/", {
      params: {
        search: userSearchQuery.value,
      },
    });

    users.value = data.value;
  } catch (error) {
    console.error("Failed to fetch users:", error);
    users.value = null;
  } finally {
    loading.value = false;
  }
};

const debounceTimeout = ref<number | null>(null);
watch(userSearchQuery, () => {
  if (debounceTimeout.value) {
    clearTimeout(debounceTimeout.value);
  }

  debounceTimeout.value = window.setTimeout(() => {
    fetchUsers();
  }, 1000);
});
</script>

<template>
  <div class="flex flex-col">
    <div class="flex justify-center mt-12">
      <UInput
        v-model="userSearchQuery"
        placeholder="Search users"
        size="xlg"
        @keyup.enter="fetchUsers"
        class="basis-3/4"
      />
    </div>

    <div class="mt-12">
      <div v-if="loading" class="text-center">Loading...</div>
      <div v-else-if="users && users.length > 0">
        <div>Found {{ users.length }} users</div>
        <UserPreviewGrid :users="users" class="my-4" />
      </div>
      <div v-else-if="users?.length === 0" class="text-center">No users found</div>
    </div>
  </div>
</template>

