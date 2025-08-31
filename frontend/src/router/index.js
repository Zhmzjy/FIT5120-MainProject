import { createRouter, createWebHistory } from 'vue-router'
import seasonalRoutes from './seasonal.js'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../pages/Home.vue')
  },
  {
    path: '/learn-wildlife',
    name: 'LearnWildlife',
    component: () => import('../pages/LearnWildlife.vue')
  },
  {
    path: '/find-zoo',
    name: 'FindZoo',
    component: () => import('../pages/FindZoo.vue')
  },
  ...seasonalRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

export default router
