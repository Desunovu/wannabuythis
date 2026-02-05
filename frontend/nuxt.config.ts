// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: true },
  modules: ["@nuxt/ui", "nuxt-open-fetch", "@sidebase/nuxt-auth"],
  css: ["~/assets/css/main.css"],
  compatibilityDate: "2024-07-20",

  runtimeConfig: {
    public: {
      apiURL: "/api",
      tokenLifetime: 24 * 60 * 60, // 24 hours in seconds
    }
  },

  openFetch: {
    disableNuxtPlugin: true,
    clients: {
      backend: {
        baseURL: process.env.NUXT_PUBLIC_API_URL || "/api",
        schema: "./openapi.json",
      },
    },
  },
  auth: {
    baseURL: process.env.NUXT_PUBLIC_API_URL || "/api",
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
        maxAgeInSeconds: Number(process.env.NUXT_PUBLIC_TOKEN_LIFETIME) || 24 * 60 * 60,
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
