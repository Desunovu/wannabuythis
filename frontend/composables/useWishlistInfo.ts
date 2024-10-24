import type { components } from "#build/types/open-fetch/schemas/backend.js";

export function useWishlistInfo(
  wishlist: components["schemas"]["WishlistResponse"] | null
) {
  const creationDate = computed(() => {
    if (!wishlist) {
      return "";
    }
    return `Created at ${new Date(wishlist.created_at).toLocaleDateString()}`;
  });

  const archivedText = computed(() => {
    if (!wishlist) {
      return "";
    }
    if (wishlist.is_archived) {
      return "(archived)";
    }
    return "";
  });

  const itemsAmountText = computed(() => {
    if (!wishlist) {
      return "";
    }
    if (wishlist.items.length === 1) {
      return "1 item";
    }
    return `${wishlist.items.length} items`;
  });

  return {
    creationDate,
    archivedText,
    itemsAmountText
  };
}
