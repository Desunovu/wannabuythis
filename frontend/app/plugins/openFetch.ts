export default defineNuxtPlugin({
  name: 'fetch-interceptor',
  enforce: 'pre',
    setup: (nuxtApp) => {
      nuxtApp.hook('openFetch:onRequest', (ctx) => {
        if (!ctx.options.headers.get('Authorization')) {
          const { token } = useAuth()
          if (token) {
              ctx.options.headers.set('Authorization', `${token.value}`)
          }
        }
      })

        nuxtApp.hook('openFetch:onResponseError', (ctx) => {
        const toast = useToast()
        const status = ctx.response?.status
        if (status === 401) {
          toast.add({
            title: 'Unauthorized',
            description: 'Please log in to continue',
            color: 'red'
          })
          const { signOut } = useAuth()
          signOut()
          navigateTo('/login')
        } else if (status >= 500) {
          toast.add({
            title: 'Server Error',
            description: 'Something went wrong on our end',
            color: 'red'
          })
        }
      })
  },
})
