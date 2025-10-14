import type { components } from "#build/types/open-fetch/schemas/backend.js";

export function useWishlistItemStyles(
  wishlistItem: components["schemas"]["WishlistItemResponse"] | null
) {
  const priorityColor = computed(() => {
    const priorities = {
      0: "text-neutral-500",
      1: "text-yellow-500",
      2: "text-orange-500",
      3: "text-red-500",
    };

    if (!wishlistItem) {
      return "text-neutral-500";
    }

    return priorities[wishlistItem.priority];
  });

  const priorityText = computed(() => {
    const priorities = {
      0: "",
      1: "Low priority",
      2: "Medium priority",
      3: "High priority",
    };
    if (!wishlistItem) {
      return "";
    }

    return priorities[wishlistItem.priority];
  });
  const amountText = computed(() => {
    if (!wishlistItem) {
      return "";
    }

    if (wishlistItem.measurement_unit === "piece") {
      if (wishlistItem.quantity === 1) {
        return "1 piece";
      }
      return `${wishlistItem.quantity} pieces`;
    }

    return `${wishlistItem.quantity} ${wishlistItem.measurement_unit}`;
  });

  return {
    priorityColor,
    priorityText,
    amountText,
  };
}
