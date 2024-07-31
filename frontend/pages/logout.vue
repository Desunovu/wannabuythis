<script setup lang="ts">
const { signOut } = useAuth();
signOut({ callbackUrl: "/login" });
</script>

<template></template>
