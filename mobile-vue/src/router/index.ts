import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', redirect: '/home' },
    { path: '/home', name: 'home', component: () => import('../pages/Home.vue') },
    { path: '/map', name: 'map', component: () => import('../pages/MapView.vue') },
    { path: '/merchant/:id', name: 'merchant-detail', component: () => import('../pages/MerchantDetail.vue') },
    { path: '/events', name: 'events', component: () => import('../pages/Events.vue') },
    { path: '/event/:id', name: 'event-detail', component: () => import('../pages/EventDetail.vue') },
    { path: '/event/:id/pay', name: 'event-payment', component: () => import('../pages/EventPayment.vue') },
    { path: '/rankings', name: 'rankings', component: () => import('../pages/Rankings.vue') },
    { path: '/news', name: 'news', component: () => import('../pages/NewsList.vue') },
    { path: '/news/:id', name: 'news-detail', component: () => import('../pages/NewsDetail.vue') },
    { path: '/clubs', name: 'clubs', component: () => import('../pages/ClubList.vue') },
    { path: '/club/:id', name: 'club-detail', component: () => import('../pages/ClubDetail.vue') },
    { path: '/club/:id/chat', name: 'club-chat', component: () => import('../pages/ClubChat.vue') },
    { path: '/profile', name: 'profile', component: () => import('../pages/Profile.vue') },
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
