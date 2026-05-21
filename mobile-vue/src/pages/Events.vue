<template>
  <div class="page events-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-title">赛事</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tab-row">
      <div
        v-for="tab in tabs"
        :key="tab"
        class="tab-item"
        :class="{ active: activeTab === tab }"
        @click="activeTab = tab"
      >{{ tab }}</div>
    </div>

    <!-- Event List -->
    <div class="event-list">
      <div v-for="event in filteredEvents" :key="event.id" class="event-card" @click="$router.push(`/event/${event.id}`)">
        <div class="event-banner" :style="{ background: event.bannerColor }">
          <div class="event-badge" :class="event.statusClass">{{ event.status }}</div>
        </div>
        <div class="event-info">
          <h3 class="event-name">{{ event.name }}</h3>
          <div class="event-details">
            <div class="event-detail">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              <span>{{ event.date }}</span>
            </div>
            <div class="event-detail">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              <span>{{ event.location }}</span>
            </div>
          </div>
          <div class="event-bottom">
            <div class="event-price">
              <span class="price-label">报名费</span>
              <span class="price-value">¥{{ event.price }}</span>
              <span class="price-unit">{{ event.priceUnit }}</span>
            </div>
            <div class="event-capacity">
              <span class="capacity-current">{{ event.current }}</span>
              <span class="capacity-sep">/</span>
              <span class="capacity-total">{{ event.total }}人</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom spacer -->
    <div class="bottom-spacer"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const activeTab = ref('全部')
const tabs = ['全部', '报名中', '进行中', '已结束']

const events = [
  {
    id: 1,
    name: '2024南京市掼蛋精英邀请赛',
    date: '2024年3月15日 14:00',
    location: '同庆楼·掼蛋主题餐厅',
    price: 200,
    priceUnit: '/人',
    current: 96,
    total: 128,
    status: '报名中',
    statusClass: 'status-open',
    bannerColor: 'linear-gradient(135deg, #8B1A2B, #C62828)'
  },
  {
    id: 2,
    name: '金陵杯·掼蛋争霸赛',
    date: '2024年3月20日 09:00',
    location: '金陵饭店国际会议中心',
    price: 500,
    priceUnit: '/人',
    current: 256,
    total: 256,
    status: '进行中',
    statusClass: 'status-active',
    bannerColor: 'linear-gradient(135deg, #1565C0, #42A5F5)'
  },
  {
    id: 3,
    name: '社区友谊掼蛋赛（第12期）',
    date: '2024年3月8日 14:00',
    location: '鼓楼区文化活动中心',
    price: 50,
    priceUnit: '/人',
    current: 32,
    total: 32,
    status: '已结束',
    statusClass: 'status-ended',
    bannerColor: 'linear-gradient(135deg, #616161, #9E9E9E)'
  },
  {
    id: 4,
    name: '江苏省掼蛋联赛·南京站',
    date: '2024年4月1日 09:00',
    location: '南京奥体中心',
    price: 1000,
    priceUnit: '/人',
    current: 48,
    total: 512,
    status: '报名中',
    statusClass: 'status-open',
    bannerColor: 'linear-gradient(135deg, #6B0F1F, #9B1B30)'
  },
  {
    id: 5,
    name: '企业团建掼蛋挑战赛',
    date: '2024年3月25日 13:30',
    location: '紫金山庄·宴会厅',
    price: 100,
    priceUnit: '/人',
    current: 60,
    total: 64,
    status: '报名中',
    statusClass: 'status-open',
    bannerColor: 'linear-gradient(135deg, #E65100, #FF9800)'
  },
]

const filteredEvents = computed(() => {
  if (activeTab.value === '全部') return events
  return events.filter(e => e.status === activeTab.value)
})
</script>

<style scoped>
.events-page {
  background: var(--bg-page);
  min-height: 100vh;
}

.header {
  background: var(--gradient-header);
  padding: var(--safe-area-top) var(--spacing-lg) 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  height: var(--header-height);
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-white);
}

.tab-row {
  display: flex;
  background: var(--bg-card);
  padding: 12px var(--spacing-lg);
  gap: 8px;
  border-bottom: 1px solid var(--border-lighter);
}

.tab-item {
  padding: 6px 16px;
  border-radius: var(--radius-full);
  font-size: 13px;
  color: var(--text-secondary);
  background: #f5f5f5;
  transition: all 0.2s;
}

.tab-item.active {
  background: var(--color-primary);
  color: white;
}

.event-list {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.event-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-card);
}

.event-banner {
  height: 80px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.event-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 11px;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  font-weight: 500;
}

.status-open {
  background: rgba(198, 40, 40, 0.9);
  color: white;
}

.status-active {
  background: rgba(21, 101, 192, 0.9);
  color: white;
}

.status-ended {
  background: rgba(117, 117, 117, 0.9);
  color: white;
}

.event-info {
  padding: 14px;
}

.event-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.event-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.event-detail {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-secondary);
}

.event-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 10px;
  border-top: 1px solid var(--border-lighter);
}

.event-price {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-label {
  font-size: 12px;
  color: var(--text-tertiary);
}

.price-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-price);
}

.price-unit {
  font-size: 12px;
  color: var(--text-tertiary);
}

.event-capacity {
  font-size: 12px;
  color: var(--text-secondary);
}

.capacity-current {
  font-weight: 600;
  color: var(--color-primary);
}

.bottom-spacer {
  height: calc(var(--tabbar-height) + 20px);
}
</style>
