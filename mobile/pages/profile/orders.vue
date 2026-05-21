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

    <!-- 订单列表 -->
    <scroll-view scroll-y class="order-list">
      <view class="order-card" v-for="order in filteredOrders" :key="order.id">
        <view class="order-header">
          <text class="order-type">{{ order.type }}</text>
          <view class="order-status" :class="order.statusClass">
            <text class="status-text">{{ order.status }}</text>
          </view>
        </view>

        <view class="order-body">
          <view class="order-cover">
            <text class="cover-emoji">{{ order.emoji }}</text>
          </view>
          <view class="order-info">
            <text class="order-name">{{ order.name }}</text>
            <text class="order-date">{{ order.date }}</text>
            <text class="order-location">{{ order.location }}</text>
          </view>
        </view>

        <view class="order-footer">
          <text class="order-fee">¥{{ order.fee }}</text>
          <view class="order-action" v-if="order.actionText" @tap="handleAction(order)">
            <text class="action-text">{{ order.actionText }}</text>
          </view>
        </view>
      </view>

      <view class="empty-state" v-if="filteredOrders.length === 0">
        <text class="empty-text">暂无记录</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const activeFilter = ref('all')

const filterTabs = [
  { label: '全部', value: 'all' },
  { label: '报名中', value: 'enrolled' },
  { label: '进行中', value: 'ongoing' },
  { label: '已结束', value: 'finished' },
]

const orders = ref([
  {
    id: '1',
    type: '赛事报名',
    emoji: '🏆',
    name: '深掼会·2024南京城市精英赛',
    date: '2024-03-15 09:00',
    location: '南京奥体中心',
    fee: '200.00',
    status: '报名成功',
    statusClass: 'enrolled',
    filter: 'enrolled',
    actionText: '查看详情',
  },
  {
    id: '2',
    type: '赛事报名',
    emoji: '💰',
    name: '金融行业精英对抗赛',
    date: '2024-03-25 10:00',
    location: '南京国际会议中心',
    fee: '300.00',
    status: '报名成功',
    statusClass: 'enrolled',
    filter: 'enrolled',
    actionText: '查看详情',
  },
  {
    id: '3',
    type: '俱乐部赛事',
    emoji: '⚡',
    name: '龙虎山俱乐部月度积分赛',
    date: '2024-03-10 19:00',
    location: '龙虎山茶馆·赛事厅',
    fee: '50.00',
    status: '进行中',
    statusClass: 'ongoing',
    filter: 'ongoing',
    actionText: '查看战况',
  },
  {
    id: '4',
    type: '赛事报名',
    emoji: '🌟',
    name: '深掼会·新手入门友谊赛',
    date: '2024-03-08 14:00',
    location: '紫金阁精品牌室',
    fee: '0.00',
    status: '已结束',
    statusClass: 'finished',
    filter: 'finished',
    actionText: '查看成绩',
  },
  {
    id: '5',
    type: '套餐购买',
    emoji: '🎴',
    name: '金陵会所·畅玩套餐',
    date: '2024-03-01',
    location: '金陵棋牌会所',
    fee: '128.00',
    status: '已使用',
    statusClass: 'finished',
    filter: 'finished',
    actionText: '',
  },
])

const filteredOrders = computed(() => {
  if (activeFilter.value === 'all') return orders.value
  return orders.value.filter((o) => o.filter === activeFilter.value)
})

function handleAction(order: any) {
  uni.showToast({ title: `正在查看「${order.name}」`, icon: 'none' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
}

.filter-tabs {
  display: flex;
  padding: 24rpx 32rpx;
  gap: 16rpx;
}

.filter-tab {
  padding: 14rpx 28rpx;
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

.order-list {
  padding: 0 32rpx;
  height: calc(100vh - 120rpx);
}

.order-card {
  background-color: #2a2a3e;
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 16rpx;
}

.order-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.order-type {
  font-size: 22rpx;
  color: #6b6b80;
}

.order-status {
  padding: 4rpx 14rpx;
  border-radius: 8rpx;
}

.order-status.enrolled {
  background-color: rgba(16, 185, 129, 0.12);
}

.order-status.ongoing {
  background-color: rgba(59, 130, 246, 0.12);
}

.order-status.finished {
  background-color: rgba(107, 107, 128, 0.12);
}

.status-text {
  font-size: 22rpx;
  color: #10b981;
}

.order-status.ongoing .status-text {
  color: #3b82f6;
}

.order-status.finished .status-text {
  color: #6b6b80;
}

.order-body {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.order-cover {
  width: 80rpx;
  height: 80rpx;
  background: linear-gradient(135deg, #32324a 0%, #1e1e32 100%);
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16rpx;
}

.cover-emoji {
  font-size: 36rpx;
}

.order-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.order-name {
  font-size: 28rpx;
  color: #f5f5f5;
  font-weight: 500;
}

.order-date {
  font-size: 22rpx;
  color: #6b6b80;
}

.order-location {
  font-size: 22rpx;
  color: #6b6b80;
}

.order-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16rpx;
  border-top: 1rpx solid #3a3a50;
}

.order-fee {
  font-size: 30rpx;
  font-weight: 600;
  color: #f6c342;
}

.order-action {
  border: 1rpx solid rgba(246, 195, 66, 0.5);
  border-radius: 12rpx;
  padding: 10rpx 24rpx;
}

.action-text {
  font-size: 24rpx;
  color: #f6c342;
}

.empty-state {
  padding: 100rpx 0;
  text-align: center;
}

.empty-text {
  font-size: 28rpx;
  color: #6b6b80;
}
</style>
