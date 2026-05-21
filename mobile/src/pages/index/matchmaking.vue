<template>
  <view class="page">
    <!-- 筛选标签 -->
    <view class="filter-tabs">
      <view
        class="filter-tab"
        :class="{ active: activeFilter === tab.value }"
        v-for="tab in filterTabs"
        :key="tab.value"
        @tap="activeFilter = tab.value"
      >
        <text class="filter-tab-text" :class="{ active: activeFilter === tab.value }">{{ tab.label }}</text>
      </view>
    </view>

    <!-- 组局列表 -->
    <scroll-view scroll-y class="match-list">
      <view class="match-card" v-for="match in filteredMatches" :key="match.id">
        <view class="match-header">
          <text class="match-title">{{ match.title }}</text>
          <view class="match-status" :class="match.statusClass">
            <text class="status-text">{{ match.status }}</text>
          </view>
        </view>

        <view class="match-details">
          <view class="detail-item">
            <text class="detail-icon">🕐</text>
            <text class="detail-text">{{ match.time }}</text>
          </view>
          <view class="detail-item">
            <text class="detail-icon">📍</text>
            <text class="detail-text">{{ match.location }}</text>
          </view>
          <view class="detail-item">
            <text class="detail-icon">👥</text>
            <text class="detail-text">{{ match.currentPlayers }}/{{ match.maxPlayers }}人</text>
          </view>
          <view class="detail-item" v-if="match.deposit">
            <text class="detail-icon">💰</text>
            <text class="detail-text">押金 ¥{{ match.deposit }}</text>
          </view>
        </view>

        <view class="match-footer">
          <view class="match-tags">
            <view class="industry-tag" v-if="match.industry">
              <text class="industry-tag-text">{{ match.industry }}</text>
            </view>
            <view class="level-tag" v-if="match.level">
              <text class="level-tag-text">{{ match.level }}</text>
            </view>
          </view>
          <view class="join-btn" @tap="handleJoin(match)">
            <text class="join-btn-text">加入</text>
          </view>
        </view>
      </view>

      <view class="empty-hint" v-if="filteredMatches.length === 0">
        <text class="empty-text">暂无组局信息</text>
      </view>
    </scroll-view>

    <!-- FAB按钮 -->
    <view class="fab-btn" @tap="goCreate">
      <text class="fab-icon">+</text>
      <text class="fab-text">发起组局</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const activeFilter = ref('all')

const filterTabs = [
  { label: '全部', value: 'all' },
  { label: '今天', value: 'today' },
  { label: '明天', value: 'tomorrow' },
  { label: '本周', value: 'week' },
]

const matches = ref([
  {
    id: '1',
    title: '商务精英掼蛋局',
    time: '今天 20:00',
    location: '金陵棋牌会所 VIP3',
    currentPlayers: 3,
    maxPlayers: 4,
    deposit: 100,
    industry: '金融',
    level: 'A段位',
    status: '差1人',
    statusClass: 'urgent',
    filter: 'today',
  },
  {
    id: '2',
    title: '周末休闲局·新手友好',
    time: '明天 14:00',
    location: '龙虎山茶馆·掼蛋区',
    currentPlayers: 2,
    maxPlayers: 4,
    deposit: 0,
    industry: '不限',
    level: 'B段位以上',
    status: '差2人',
    statusClass: 'normal',
    filter: 'tomorrow',
  },
  {
    id: '3',
    title: 'IT行业掼蛋交流',
    time: '今天 19:30',
    location: '紫金阁精品牌室 2号桌',
    currentPlayers: 3,
    maxPlayers: 4,
    deposit: 50,
    industry: '互联网',
    level: 'A+段位',
    status: '差1人',
    statusClass: 'urgent',
    filter: 'today',
  },
  {
    id: '4',
    title: '教育圈掼友聚会',
    time: '周六 15:00',
    location: '秦淮雅集·商务包间',
    currentPlayers: 1,
    maxPlayers: 4,
    deposit: 0,
    industry: '教育',
    level: '不限',
    status: '差3人',
    statusClass: 'normal',
    filter: 'week',
  },
  {
    id: '5',
    title: '高段位竞技对抗',
    time: '周日 10:00',
    location: '玄武湖畔会所 竞技厅',
    currentPlayers: 2,
    maxPlayers: 4,
    deposit: 200,
    industry: '不限',
    level: 'S段位',
    status: '差2人',
    statusClass: 'normal',
    filter: 'week',
  },
])

const filteredMatches = computed(() => {
  if (activeFilter.value === 'all') return matches.value
  return matches.value.filter((m) => m.filter === activeFilter.value)
})

function handleJoin(match: any) {
  uni.showToast({ title: `已申请加入「${match.title}」`, icon: 'none' })
}

function goCreate() {
  uni.navigateTo({ url: '/pages/index/create-match' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 160rpx;
}

.filter-tabs {
  display: flex;
  padding: 24rpx 32rpx;
  gap: 16rpx;
}

.filter-tab {
  padding: 14rpx 32rpx;
  border-radius: 32rpx;
  background-color: #2a2a3e;
}

.filter-tab.active {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
}

.filter-tab-text {
  font-size: 26rpx;
  color: #b0b0c0;
}

.filter-tab-text.active {
  color: #1a1a2e;
  font-weight: 600;
}

.match-list {
  height: calc(100vh - 140rpx);
  padding: 0 32rpx;
}

.match-card {
  background-color: #2a2a3e;
  border-radius: 24rpx;
  padding: 28rpx;
  margin-bottom: 20rpx;
}

.match-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.match-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
  flex: 1;
}

.match-status {
  padding: 6rpx 16rpx;
  border-radius: 8rpx;
}

.match-status.urgent {
  background-color: rgba(239, 68, 68, 0.15);
}

.match-status.normal {
  background-color: rgba(246, 195, 66, 0.12);
}

.status-text {
  font-size: 22rpx;
  color: #f6c342;
}

.match-status.urgent .status-text {
  color: #ef4444;
}

.match-details {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
  margin-bottom: 20rpx;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.detail-icon {
  font-size: 24rpx;
}

.detail-text {
  font-size: 26rpx;
  color: #b0b0c0;
}

.match-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16rpx;
  border-top: 1rpx solid #3a3a50;
}

.match-tags {
  display: flex;
  gap: 12rpx;
}

.industry-tag {
  background-color: rgba(59, 130, 246, 0.12);
  border-radius: 8rpx;
  padding: 6rpx 14rpx;
}

.industry-tag-text {
  font-size: 20rpx;
  color: #3b82f6;
}

.level-tag {
  background-color: rgba(246, 195, 66, 0.12);
  border-radius: 8rpx;
  padding: 6rpx 14rpx;
}

.level-tag-text {
  font-size: 20rpx;
  color: #f6c342;
}

.join-btn {
  border: 1rpx solid rgba(246, 195, 66, 0.5);
  border-radius: 12rpx;
  padding: 12rpx 32rpx;
}

.join-btn-text {
  font-size: 26rpx;
  color: #f6c342;
  font-weight: 500;
}

/* FAB按钮 */
.fab-btn {
  position: fixed;
  bottom: 120rpx;
  right: 32rpx;
  display: flex;
  align-items: center;
  gap: 8rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 40rpx;
  padding: 20rpx 32rpx;
  box-shadow: 0 8px 24px rgba(246, 195, 66, 0.3);
}

.fab-icon {
  font-size: 32rpx;
  color: #1a1a2e;
  font-weight: 700;
}

.fab-text {
  font-size: 26rpx;
  color: #1a1a2e;
  font-weight: 600;
}

.empty-hint {
  padding: 100rpx 0;
  text-align: center;
}

.empty-text {
  font-size: 28rpx;
  color: #6b6b80;
}
</style>
