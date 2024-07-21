<script setup lang="ts">
import type { FormError, FormSubmitEvent } from "#ui/types";

const { $backend } = useNuxtApp();

const state = reactive({
  username: undefined,
  email: undefined,
  password: undefined,
  confirmPassword: undefined,
});

const validate = (state: any): FormError[] => {
  const errors = [];
  if (!state.username) errors.push({ path: "username", message: "Required" });
  if (!state.email) errors.push({ path: "email", message: "Required" });
  if (!state.password) errors.push({ path: "password", message: "Required" });
  if (state.password !== state.confirmPassword) errors.push({ path: "confirmPassword", message: "Passwords do not match" });
  return errors;
};

async function onSubmit(event: FormSubmitEvent<any>) {
  const response = await $backend("/auth/register", {
    method: "POST",
    body: event.data
  })
  console.log(response);
}
</script>

<template>
  <UForm :validate="validate" :state="state" class="space-y-4" @submit="onSubmit">
    <UFormGroup label="Username" name="username">
      <UInput v-model="state.username" />
    </UFormGroup>

    <UFormGroup label="Email" name="email">
      <UInput v-model="state.email" />
    </UFormGroup>

    <UFormGroup label="Password" name="password">
      <UInput v-model="state.password" type="password" />
    </UFormGroup>

    <UFormGroup label="Confirm Password" name="confirmPassword">
      <UInput v-model="state.confirmPassword" type="password" />
    </UFormGroup>

    <div class="flex justify-end">
      <UButton type="submit"> Register </UButton>
    </div>
  </UForm>
</template>
