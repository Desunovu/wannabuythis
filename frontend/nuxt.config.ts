// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxt/ui", "nuxt-open-fetch", "@sidebase/nuxt-auth"],
  compatibilityDate: "2024-07-20",
  openFetch: {
    disableNuxtPlugin: true,
    clients: {
      backend: {
        baseURL: process.env.BACKEND_URL || "/api",
        schema: process.env.BACKEND_URL+"/schema.json" || "/api/schema.json",
      },
    },
  },
  auth: {
    baseURL: process.env.BACKEND_URL || "/api",
    globalAppMiddleware: {
      isEnabled: true,
      addDefaultCallbackUrl: "login",
    },
    provider: {
      type: "local",
      endpoints: {
        signIn: { path: "auth/login", method: "post" },
        signOut: false,
        signUp: { path: "auth/register", method: "post" },
        getSession: { path: "users/me", method: "get" },
      },
      token: {
        signInResponseTokenPointer: "/access_token",
      },
      session: {
        dataType: {
          username: "string",
          email: "string",
          is_active: "boolean",
        },
      },
    },
  },
});
