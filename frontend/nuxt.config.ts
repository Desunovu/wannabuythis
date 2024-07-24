// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxt/ui", "nuxt-open-fetch", "@sidebase/nuxt-auth"],
  compatibilityDate: "2024-07-20",
  openFetch: {
    clients: {
      backend: {
        baseURL: "http://localhost:8000",
        schema: "http://localhost:8000/openapi.json"
      }
    }
  }
})