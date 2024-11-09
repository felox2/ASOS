import { createRouter, createWebHistory } from 'vue-router'
import { handleHotUpdate, routes } from 'vue-router/auto-routes'
import { useAuthStore } from './stores/auth'

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

// router.beforeEach((to, from, next) => {
//   const authStore = useAuthStore()

//   if (to.meta.guest && authStore.user && to.path !== '/') {
//     next('/')
//     return
//   }
//   if (!to.meta.guest && !authStore.user && to.path !== '/auth/login') {
//     next('/auth/login')
//     return
//   }

//   return next()
// })

// This will update routes at runtime without reloading the page
if (import.meta.hot) {
  handleHotUpdate(router)
}