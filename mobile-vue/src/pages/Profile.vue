<template>
  <div class="page profile-page">
    <!-- Profile Header -->
    <div class="profile-header">
      <div class="header-bg"></div>
      <div class="profile-info">
        <div class="avatar-wrapper">
          <div class="avatar">
            <span>王</span>
          </div>
          <div class="avatar-badge">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="#FFD700"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          </div>
        </div>
        <h1 class="user-name">掼蛋小王子</h1>
        <p class="user-id">ID: GD20240001</p>
        
        <!-- Stats Row -->
        <div class="stats-row">
          <div class="stat-item">
            <span class="stat-value">2680</span>
            <span class="stat-label">ELO</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">128</span>
            <span class="stat-label">场次</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-value">72%</span>
            <span class="stat-label">胜率</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Wallet Card -->
    <div class="wallet-card">
      <div class="wallet-header">
        <span class="wallet-title">我的钱包</span>
        <span class="wallet-more">查看详情 ›</span>
      </div>
      <div class="wallet-balance">
        <div class="balance-item">
          <span class="balance-value">¥2,680</span>
          <span class="balance-label">余额</span>
        </div>
        <div class="balance-item">
          <span class="balance-value">1,200</span>
          <span class="balance-label">积分</span>
        </div>
        <div class="balance-item">
          <span class="balance-value">3</span>
          <span class="balance-label">优惠券</span>
        </div>
      </div>
    </div>

    <!-- Menu List -->
    <div class="menu-card">
      <div v-for="item in menuItems" :key="item.label" class="menu-item" @click="handleMenu(item)">
        <div class="menu-icon" :style="{ background: item.iconBg }">
          <div v-html="item.icon"></div>
        </div>
        <span class="menu-label">{{ item.label }}</span>
        <div class="menu-right">
          <span v-if="item.badge" class="menu-badge">{{ item.badge }}</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </div>
      </div>
    </div>

    <!-- Second Menu -->
    <div class="menu-card">
      <div v-for="item in settingsItems" :key="item.label" class="menu-item">
        <div class="menu-icon" :style="{ background: item.iconBg }">
          <div v-html="item.icon"></div>
        </div>
        <span class="menu-label">{{ item.label }}</span>
        <div class="menu-right">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </div>
      </div>
    </div>

    <!-- Bottom spacer -->
    <div class="bottom-spacer"></div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const menuItems = [
  {
    label: '赛事记录',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/></svg>',
    iconBg: 'linear-gradient(135deg, #C62828, #E53935)',
    badge: '12',
    route: '/events'
  },
  {
    label: '购买记录',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>',
    iconBg: 'linear-gradient(135deg, #1565C0, #42A5F5)',
    badge: '',
    route: ''
  },
  {
    label: '荣誉徽章',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89L17 22l-5-3-5 3 1.523-9.11"/></svg>',
    iconBg: 'linear-gradient(135deg, #E65100, #FF9800)',
    badge: '5',
    route: ''
  },
  {
    label: '找掼友',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    iconBg: 'linear-gradient(135deg, #2E7D32, #66BB6A)',
    badge: '',
    route: ''
  },
  {
    label: '我的俱乐部',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8"><path d="M12 2L4 7v6c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V7l-8-5z"/></svg>',
    iconBg: 'linear-gradient(135deg, #6A1B9A, #AB47BC)',
    badge: '',
    route: '/clubs'
  },
]

const settingsItems = [
  {
    label: '消息通知',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    iconBg: 'linear-gradient(135deg, #F44336, #EF5350)'
  },
  {
    label: '帮助与反馈',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    iconBg: 'linear-gradient(135deg, #546E7A, #78909C)'
  },
  {
    label: '设置',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    iconBg: 'linear-gradient(135deg, #455A64, #607D8B)'
  },
]

function handleMenu(item: any) {
  if (item.route) {
    router.push(item.route)
  }
}
</script>

<style scoped>
.profile-page {
  background: var(--bg-page);
  min-height: 100vh;
}

.profile-header {
  position: relative;
  padding-bottom: 20px;
}

.header-bg {
  height: 180px;
  background: var(--gradient-header);
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}

.profile-info {
  position: relative;
  padding: calc(var(--safe-area-top) + 30px) var(--spacing-lg) 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-wrapper {
  position: relative;
  margin-bottom: 12px;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #FFD700, #FFA000);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28px;
  font-weight: 700;
  border: 3px solid white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.avatar-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.user-name {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin-bottom: 4px;
}

.user-id {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.75);
  margin-bottom: 16px;
}

.stats-row {
  display: flex;
  align-items: center;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px 24px;
  box-shadow: var(--shadow-card);
  gap: 20px;
  width: 100%;
  justify-content: space-around;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 11px;
  color: var(--text-tertiary);
}

.stat-divider {
  width: 1px;
  height: 28px;
  background: var(--border-lighter);
}

.wallet-card {
  background: var(--bg-card);
  margin: 12px var(--spacing-lg);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-card);
}

.wallet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.wallet-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.wallet-more {
  font-size: 12px;
  color: var(--text-tertiary);
}

.wallet-balance {
  display: flex;
  justify-content: space-around;
}

.balance-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.balance-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-price);
}

.balance-label {
  font-size: 11px;
  color: var(--text-tertiary);
}

.menu-card {
  background: var(--bg-card);
  margin: 12px var(--spacing-lg);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-lighter);
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-icon {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.menu-label {
  flex: 1;
  font-size: 14px;
  color: var(--text-primary);
}

.menu-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.menu-badge {
  font-size: 11px;
  padding: 2px 8px;
  background: #fff0f0;
  color: var(--color-primary);
  border-radius: var(--radius-full);
}

.bottom-spacer {
  height: calc(var(--tabbar-height) + 20px);
}
</style>
