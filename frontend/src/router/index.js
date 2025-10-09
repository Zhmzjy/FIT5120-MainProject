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
    path: '/ai-challenge',
    name: 'AIChallenge',
    component: () => import('../pages/AIChallenge.vue')
  },
  {
    path: '/daily-wildle',
    name: 'DailyWildle',
    component: () => import('../pages/DailyWildle.vue')
  },
  {
    path: '/conservation',
    name: 'Conservation',
    component: () => import('../pages/Conservation.vue')
  },
  {
    path: '/yearly-analysis',
    name: 'YearlyAnalysis',
    component: () => import('../pages/YearlyAnalysis.vue')
  },
  {
    path: '/audio-game',
    name: 'AudioMatchingGame',
    component: () => import('../pages/AudioMatchingGame.vue')
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
