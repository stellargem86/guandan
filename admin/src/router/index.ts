import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores'

// Admin portal routes (Super Admin)
const adminRoutes: RouteRecordRaw[] = [
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/index.vue'),
    meta: { title: '仪表盘', portal: 'admin', icon: 'dashboard' },
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('@/views/users/index.vue'),
    meta: { title: '用户管理', portal: 'admin', icon: 'users' },
  },
  {
    path: '/content',
    name: 'Content',
    component: () => import('@/views/content/index.vue'),
    meta: { title: '内容审核', portal: 'admin', icon: 'content' },
  },
  {
    path: '/finance',
    name: 'Finance',
    component: () => import('@/views/finance/index.vue'),
    meta: { title: '财务管理', portal: 'admin', icon: 'finance' },
  },
  {
    path: '/events',
    name: 'Events',
    component: () => import('@/views/events/index.vue'),
    meta: { title: '赛事管理', portal: 'admin', icon: 'events' },
  },
  {
    path: '/merchants',
    name: 'Merchants',
    component: () => import('@/views/merchants/index.vue'),
    meta: { title: '商户管理', portal: 'admin', icon: 'merchants' },
  },
  {
    path: '/clubs',
    name: 'Clubs',
    component: () => import('@/views/clubs/index.vue'),
    meta: { title: '俱乐部管理', portal: 'admin', icon: 'clubs' },
  },
  {
    path: '/ads',
    name: 'Ads',
    component: () => import('@/views/ads/index.vue'),
    meta: { title: '广告管理', portal: 'admin', icon: 'ads' },
  },
  {
    path: '/config',
    name: 'Config',
    component: () => import('@/views/config/index.vue'),
    meta: { title: '系统配置', portal: 'admin', icon: 'config' },
  },
]

// Merchant portal routes
const merchantRoutes: RouteRecordRaw[] = [
  {
    path: '/merchant-portal',
    name: 'MerchantPortal',
    redirect: '/merchant-portal/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'MerchantDashboard',
        component: () => import('@/views/merchant-portal/dashboard.vue'),
        meta: { title: '商户仪表盘', portal: 'merchant', icon: 'dashboard' },
      },
      {
        path: 'verify',
        name: 'MerchantVerify',
        component: () => import('@/views/merchant-portal/verify.vue'),
        meta: { title: '核销管理', portal: 'merchant', icon: 'verify' },
      },
      {
        path: 'packages',
        name: 'MerchantPackages',
        component: () => import('@/views/merchant-portal/packages.vue'),
        meta: { title: '套餐管理', portal: 'merchant', icon: 'packages' },
      },
      {
        path: 'settlement',
        name: 'MerchantSettlement',
        component: () => import('@/views/merchant-portal/settlement.vue'),
        meta: { title: '结算提现', portal: 'merchant', icon: 'settlement' },
      },
    ],
  },
]

// Organizer portal routes
const organizerRoutes: RouteRecordRaw[] = [
  {
    path: '/organizer-portal',
    name: 'OrganizerPortal',
    redirect: '/organizer-portal/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'OrganizerDashboard',
        component: () => import('@/views/organizer-portal/dashboard.vue'),
        meta: { title: '组织者仪表盘', portal: 'organizer', icon: 'dashboard' },
      },
      {
        path: 'members',
        name: 'OrganizerMembers',
        component: () => import('@/views/organizer-portal/members.vue'),
        meta: { title: '会员管理', portal: 'organizer', icon: 'members' },
      },
      {
        path: 'events',
        name: 'OrganizerEvents',
        component: () => import('@/views/organizer-portal/events.vue'),
        meta: { title: '赛事发布', portal: 'organizer', icon: 'events' },
      },
      {
        path: 'checkin',
        name: 'OrganizerCheckin',
        component: () => import('@/views/organizer-portal/checkin.vue'),
        meta: { title: '签到管理', portal: 'organizer', icon: 'checkin' },
      },
      {
        path: 'scoreboard',
        name: 'OrganizerScoreboard',
        component: () => import('@/views/organizer-portal/scoreboard.vue'),
        meta: { title: '实时记分牌', portal: 'organizer', icon: 'scoreboard' },
      },
      {
        path: 'reports',
        name: 'OrganizerReports',
        component: () => import('@/views/organizer-portal/reports.vue'),
        meta: { title: '收入报表', portal: 'organizer', icon: 'reports' },
      },
    ],
  },
]

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login.vue'),
    meta: { title: '登录', public: true },
  },
  {
    path: '/',
    redirect: '/dashboard',
  },
  ...adminRoutes,
  ...merchantRoutes,
  ...organizerRoutes,
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/not-found.vue'),
    meta: { title: '页面未找到', public: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard
router.beforeEach((to, _from, next) => {
  // Update page title
  const title = to.meta.title as string | undefined
  document.title = title ? `${title} - 深掼会管理后台` : '深掼会管理后台'

  // Allow public routes
  if (to.meta.public) {
    next()
    return
  }

  const authStore = useAuthStore()

  // Require authentication
  if (!authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  // Portal access control
  const portal = to.meta.portal as string | undefined
  if (portal === 'admin' && !authStore.isAdmin) {
    // Non-admins cannot access admin portal
    const role = authStore.user?.role
    if (role === 'merchant') {
      next('/merchant-portal/dashboard')
    } else if (role === 'organizer') {
      next('/organizer-portal/dashboard')
    } else {
      next('/login')
    }
    return
  }

  if (portal === 'merchant' && !authStore.isMerchant && !authStore.isAdmin) {
    next('/dashboard')
    return
  }

  if (portal === 'organizer' && !authStore.isOrganizer && !authStore.isAdmin) {
    next('/dashboard')
    return
  }

  next()
})

export default router
