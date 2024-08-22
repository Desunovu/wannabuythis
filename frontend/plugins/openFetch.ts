export default defineNuxtPlugin({
  enforce: "pre", // clients will be ready to use by other plugins, Pinia stores etc.
  setup() {
    const clients = useRuntimeConfig().public.openFetch;
    const localFetch = useRequestFetch();
    const { token } = useAuth();

    return {
      provide: Object.entries(clients).reduce(
        (acc, [name, options]) => ({
          ...acc,
          [name]: createOpenFetch(
            (localOptions) => ({
              ...options,
              ...localOptions,
              onRequest(ctx) {
                ctx.options.headers = {
                  ...(ctx.options.headers || {}),
                  Authorization: `Bearer ${token}`,
                };
                return localOptions?.onRequest?.(ctx);
              },
            }),
            localFetch
          ),
        }),
        {}
      ),
    };
  },
});
