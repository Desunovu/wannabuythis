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

  return {
    creationDate,
  };
}
