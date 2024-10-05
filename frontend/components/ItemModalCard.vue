<script setup lang="ts">
import type { components } from "#build/types/open-fetch/schemas/backend.js";

const props = defineProps<{
  wishlistItem: components["schemas"]["WishlistItemResponse"];
  isOwner: boolean;
}>();

const { priorityColor, priorityText, amountText } = useWishlistItemStyles(
  props.wishlistItem
);
</script>

<template>
  <UModal>
    <UCard>
      <div class="flex flex-col items-center space-y-8">
        <div class="flex flex-col items-center space-y-2">
          <UAvatar
            class="rounded-none"
            size="3xl"
            :text="wishlistItem.name.charAt(0)"
          />
          <div class="text-2xl font-bold">{{ wishlistItem.name }}</div>
          <div>{{ amountText }}</div>
          <div :class="priorityColor">{{ priorityText }}</div>
          <div v-if="wishlistItem.is_purchased" class="text-red-600 font-bold">
            Purchased
          </div>
        </div>

        <!-- Only show actions if the user is the owner -->
        <ItemActionButtons
          v-if="isOwner"
          :wishlist-uuid="wishlistItem.wishlist_uuid"
          :wishlist-item-uuid="wishlistItem.uuid"
          :is-purchased="wishlistItem.is_purchased"
        />
      </div>
    </UCard>
  </UModal>
</template>
