<script setup lang="ts">
import type { FormError, FormSubmitEvent } from "#ui/types";

const { $backend } = useNuxtApp();

const state = reactive({
  username: undefined,
  password: undefined,
});

const validate = (state: any): FormError[] => {
  const errors = [];
  if (!state.username) errors.push({ path: "username", message: "Required" });
  if (!state.password) errors.push({ path: "password", message: "Required" });
  return errors;
};

async function onSubmit(event: FormSubmitEvent<any>) {
  const formData = new FormData()
  formData.append("username", event.data.username)
  formData.append("password", event.data.password)

  const response = await $backend("/auth/login", {
    method: "POST",
    body: formData,
  })
  console.log(response);
}
</script>

<template>
  <UForm :validate="validate" :state="state" class="space-y-4" @submit="onSubmit">
    <UFormGroup label="Username" name="username">
      <UInput v-model="state.username" />
    </UFormGroup>

    <UFormGroup label="Password" name="password">
      <UInput v-model="state.password" type="password" />
    </UFormGroup>

    <div class="flex justify-end">
      <UButton type="submit"> Submit </UButton>
    </div>
  </UForm>
</template>
