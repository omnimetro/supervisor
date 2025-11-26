import { defineRouter } from '#q-app/wrappers'
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'src/stores/auth'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  })

  // ============================================
  // Navigation Guards
  // ============================================

  /**
   * Guard de navigation pour protéger les routes qui nécessitent une authentification
   * Vérifie si l'utilisateur est connecté avant d'accéder aux routes protégées
   */
  Router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()

    // Vérifier si la route nécessite une authentification
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

    // Si la route nécessite une authentification et que l'utilisateur n'est pas connecté
    if (requiresAuth && !authStore.isAuthenticated) {
      // Rediriger vers la page de connexion avec l'URL de redirection
      next({
        path: '/auth/login',
        query: { redirect: to.fullPath }
      })
    }
    // Si l'utilisateur est connecté et essaie d'accéder à la page de connexion
    else if (to.path === '/auth/login' && authStore.isAuthenticated) {
      // Rediriger vers la page d'accueil ou la page demandée
      const redirectPath = to.query.redirect || '/'
      next(redirectPath)
    }
    // Sinon, autoriser la navigation
    else {
      next()
    }
  })

  // Guard après navigation (optionnel, pour analytics, logs, etc.)
  Router.afterEach((to, from) => {
    if (process.env.DEV) {
      console.log('🧭 Navigation:', from.path, '→', to.path)
    }
  })

  return Router
})
