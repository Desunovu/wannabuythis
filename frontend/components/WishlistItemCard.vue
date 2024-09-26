<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";
const props = defineProps<{
  wishlistItem: components["schemas"]["WishlistItemResponse"];
  isOwner: boolean;
}>();

const priorityColor = computed(() => {
  const priorities = {
    0: "text-neutral-500",
    1: "text-yellow-500",
    2: "text-orange-500",
    3: "text-red-500",
  };

  return priorities[props.wishlistItem.priority];
});

const priorityText = computed(() => {
  const priorities = {
    0: "",
    1: "Low priority",
    2: "Medium priority",
    3: "High priority",
  };

  return priorities[props.wishlistItem.priority];
});

const amountText = computed(() => {
  if (props.wishlistItem.measurement_unit === "piece") {
    if (props.wishlistItem.quantity === 1) {
      return "1 piece";
    }
    return `${props.wishlistItem.quantity} pieces`;
  }

  return `${props.wishlistItem.quantity} ${props.wishlistItem.measurement_unit}`;
});
</script>

<template>
  <UCard>
    <div class="flex flex-col items-center space-y-2 h-56">
      <UAvatar size="2xl" :text="wishlistItem.name.charAt(0)" />
      <div class="text-2xl font-bold">{{ wishlistItem.name }}</div>
      <div>{{ amountText }}</div>
      <div :class="priorityColor">{{ priorityText }}</div>
      <div v-if="wishlistItem.is_purchased" class="text-red-600 font-bold">
        Purchased
      </div>
    </div>

    <!-- Only show actions if the user is the owner -->
    <WishlistItemActions
      v-if="isOwner"
      :wishlist-uuid="wishlistItem.wishlist_uuid"
      :wishlist-item-uuid="wishlistItem.uuid"
      :is-purchased="wishlistItem.is_purchased"
    />
  </UCard>
</template>
