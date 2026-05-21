<template>
  <view class="page">
    <!-- 分类标签 -->
    <view class="category-tabs">
      <view
        class="cat-tab"
        :class="{ active: activeCategory === cat.value }"
        v-for="cat in categories"
        :key="cat.value"
        @tap="activeCategory = cat.value"
      >
        <text class="cat-tab-text" :class="{ active: activeCategory === cat.value }">{{ cat.label }}</text>
      </view>
    </view>

    <!-- 排行榜入口 -->
    <view class="ranking-entry" @tap="goRankings">
      <view class="ranking-left">
        <text class="ranking-icon">🏅</text>
        <text class="ranking-text">天梯排行榜</text>
      </view>
      <text class="ranking-arrow">查看 ›</text>
    </view>

    <!-- 赛事列表 -->
    <scroll-view scroll-y class="event-list">
      <view class="event-card" v-for="event in filteredEvents" :key="event.id" @tap="goDetail(event.id)">
        <view class="event-cover">
          <text class="event-cover-emoji">{{ event.emoji }}</text>
          <view class="event-status-badge" :class="event.statusClass">
            <text class="event-status-text">{{ event.status }}</text>
          </view>
        </view>
        <view class="event-info">
          <text class="event-title">{{ event.title }}</text>
          <view class="event-meta">
            <view class="meta-item">
              <text class="meta-icon">📅</text>
              <text class="meta-text">{{ event.date }}</text>
            </view>
            <view class="meta-item">
              <text class="meta-icon">📍</text>
              <text class="meta-text">{{ event.location }}</text>
            </view>
          </view>
          <view class="event-bottom">
            <view class="event-stats">
              <text class="event-fee">¥{{ event.fee }}</text>
              <text class="event-capacity">{{ event.enrolled }}/{{ event.capacity }}人</text>
            </view>
            <view class="event-btn" v-if="event.status === '报名中'" @tap.stop="handleEnroll(event)">
              <text class="event-btn-text">立即报名</text>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const activeCategory = ref('all')

const categories = [
  { label: '全部', value: 'all' },
  { label: '官方赛事', value: 'official' },
  { label: '商会赛事', value: 'business' },
  { label: '俱乐部赛事', value: 'club' },
]

const events = ref([
  {
    id: '1',
    title: '深掼会·2024南京城市精英赛',
    emoji: '🏆',
    date: '2024-03-15 09:00',
    location: '南京奥体中心',
    fee: 200,
    enrolled: 198,
    capacity: 256,
    status: '报名中',
    statusClass: 'enrolling',
    category: 'official',
  },
  {
    id: '2',
    title: '江苏省企业家掼蛋邀请赛',
    emoji: '🎖️',
    date: '2024-03-20 14:00',
    location: '金陵饭店·宴会厅',
    fee: 500,
    enrolled: 64,
    capacity: 128,
    status: '报名中',
    statusClass: 'enrolling',
    category: 'business',
  },
  {
    id: '3',
    title: '龙虎山俱乐部月度积分赛',
    emoji: '⚡',
    date: '2024-03-10 19:00',
    location: '龙虎山茶馆·赛事厅',
    fee: 50,
    enrolled: 32,
    capacity: 32,
    status: '进行中',
    statusClass: 'ongoing',
    category: 'club',
  },
  {
    id: '4',
    title: '深掼会·新手入门友谊赛',
    emoji: '🌟',
    date: '2024-03-08 14:00',
    location: '紫金阁精品牌室',
    fee: 0,
    enrolled: 24,
    capacity: 24,
    status: '已结束',
    statusClass: 'finished',
    category: 'official',
  },
  {
    id: '5',
    title: '金融行业精英对抗赛',
    emoji: '💰',
    date: '2024-03-25 10:00',
    location: '南京国际会议中心',
    fee: 300,
    enrolled: 56,
    capacity: 64,
    status: '报名中',
    statusClass: 'enrolling',
    category: 'business',
  },
])

const filteredEvents = computed(() => {
  if (activeCategory.value === 'all') return events.value
  return events.value.filter((e) => e.category === activeCategory.value)
})

function goDetail(id: string) {
  uni.navigateTo({ url: `/pages/events/detail?id=${id}` })
}

function goRankings() {
  uni.navigateTo({ url: '/pages/events/rankings' })
}

function handleEnroll(event: any) {
  uni.showToast({ title: `已报名「${event.title}」`, icon: 'none' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 120rpx;
}

.category-tabs {
  display: flex;
  padding: 24rpx 32rpx;
  gap: 16rpx;
  overflow-x: auto;
}

.cat-tab {
  padding: 14rpx 28rpx;
  border-radius: 32rpx;
  background-color: #2a2a3e;
  white-space: nowrap;
  flex-shrink: 0;
}

.cat-tab.active {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
}

.cat-tab-text {
  font-size: 26rpx;
  color: #b0b0c0;
}

.cat-tab-text.active {
  color: #1a1a2e;
  font-weight: 600;
}

/* 排行榜入口 */
.ranking-entry {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 32rpx 24rpx;
  padding: 24rpx;
  background: linear-gradient(135deg, rgba(246, 195, 66, 0.08) 0%, rgba(246, 195, 66, 0.03) 100%);
  border-radius: 16rpx;
  border: 1rpx solid rgba(246, 195, 66, 0.15);
}

.ranking-left {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.ranking-icon {
  font-size: 32rpx;
}

.ranking-text {
  font-size: 28rpx;
  color: #f6c342;
  font-weight: 500;
}

.ranking-arrow {
  font-size: 24rpx;
  color: #f6c342;
}

/* 赛事列表 */
.event-list {
  padding: 0 32rpx;
  height: calc(100vh - 260rpx);
}

.event-card {
  background-color: #2a2a3e;
  border-radius: 24rpx;
  overflow: hidden;
  margin-bottom: 24rpx;
}

.event-cover {
  height: 200rpx;
  background: linear-gradient(135deg, #32324a 0%, #1e1e32 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.event-cover-emoji {
  font-size: 80rpx;
}

.event-status-badge {
  position: absolute;
  top: 16rpx;
  right: 16rpx;
  padding: 6rpx 16rpx;
  border-radius: 8rpx;
}

.event-status-badge.enrolling {
  background-color: rgba(16, 185, 129, 0.15);
}

.event-status-badge.ongoing {
  background-color: rgba(59, 130, 246, 0.15);
}

.event-status-badge.finished {
  background-color: rgba(107, 107, 128, 0.15);
}

.event-status-text {
  font-size: 22rpx;
  color: #10b981;
}

.event-status-badge.ongoing .event-status-text {
  color: #3b82f6;
}

.event-status-badge.finished .event-status-text {
  color: #6b6b80;
}

.event-info {
  padding: 24rpx;
}

.event-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: 16rpx;
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
  margin-bottom: 16rpx;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.meta-icon {
  font-size: 22rpx;
}

.meta-text {
  font-size: 24rpx;
  color: #b0b0c0;
}

.event-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16rpx;
  border-top: 1rpx solid #3a3a50;
}

.event-stats {
  display: flex;
  align-items: baseline;
  gap: 16rpx;
}

.event-fee {
  font-size: 32rpx;
  font-weight: 700;
  color: #f6c342;
}

.event-capacity {
  font-size: 24rpx;
  color: #6b6b80;
}

.event-btn {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 12rpx;
  padding: 14rpx 28rpx;
}

.event-btn-text {
  font-size: 24rpx;
  color: #1a1a2e;
  font-weight: 600;
}
</style>
