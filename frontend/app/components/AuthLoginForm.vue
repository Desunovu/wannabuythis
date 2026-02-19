<script setup lang="ts">
import type { FormError, FormSubmitEvent } from "#ui/types";

const { signIn } = useAuth();
const toast = useToast();

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
  const formData = new FormData();
  formData.append("username", event.data.username);
  formData.append("password", event.data.password);
  try {
    await signIn(formData, { callbackUrl: "/" });
    toast.add({
      title: "Login Successful",
      color: "success",
      duration: 3000
    });
  } catch (error) {
    if (error.response?.status === 401) {
      toast.add({
        title: "Login Failed",
        description: "Invalid username or password",
        color: "error",
        duration: 5000,
        icon: "i-heroicons-exclamation-circle",
      });
    } else if (error.response?.status === 429) {
      toast.add({
        title: "Too Many Requests",
        description: "Please wait before trying again",
        color: "error",
        duration: 5000,
        icon: "i-heroicons-clock",
      });
    } else {
      toast.add({
        title: "Login Failed",
        description: "An error occurred during login",
        color: "error",
        duration: 5000,
        icon: "i-heroicons-exclamation-circle",
      });
    }
  }
}
</script>

<template>
  <UForm
    :validate="validate"
    :state="state"
    class="space-y-4"
    @submit="onSubmit"
  >
    <UFormField label="Username" name="username">
      <UInput v-model="state.username" />
    </UFormField>

    <UFormField label="Password" name="password">
      <UInput v-model="state.password" type="password" />
    </UFormField>

    <div class="flex justify-end">
      <UButton type="submit"> Submit </UButton>
    </div>
  </UForm>
</template>
