<template>
  <view class="page">
    <!-- 顶部标签栏 -->
    <view class="top-tabs">
      <view
        class="top-tab"
        :class="{ active: activeStatus === s.value }"
        v-for="s in statusTabs"
        :key="s.value"
        @tap="activeStatus = s.value"
      >
        <text class="top-tab-text" :class="{ active: activeStatus === s.value }">{{ s.label }}</text>
      </view>
    </view>

    <!-- 赛事列表 -->
    <scroll-view scroll-y class="event-scroll">
      <view class="event-card" v-for="event in filteredEvents" :key="event.id" @tap="goDetail(event.id)">
        <view class="event-header">
          <text class="event-title">{{ event.title }}</text>
          <view class="event-status" :class="event.statusClass">
            <text class="status-text">{{ event.statusLabel }}</text>
          </view>
        </view>
        <view class="event-info-list">
          <view class="event-info-row">
            <text class="info-icon">📅</text>
            <text class="info-text">{{ event.date }}</text>
          </view>
          <view class="event-info-row">
            <text class="info-icon">📍</text>
            <text class="info-text">{{ event.location }}</text>
          </view>
          <view class="event-info-row">
            <text class="info-icon">💰</text>
            <text class="info-text">奖金: ¥{{ event.prize }}</text>
          </view>
        </view>
        <view class="event-footer">
          <view class="event-fee-info">
            <text class="event-fee">¥{{ event.fee }}</text>
            <text class="event-capacity">{{ event.enrolled }}/{{ event.capacity }}人</text>
          </view>
          <view class="enroll-btn" v-if="event.status === 'enrolling'" @tap.stop="handleEnroll(event)">
            <text class="enroll-btn-text">立即报名</text>
          </view>
          <view class="view-btn" v-else @tap.stop="goDetail(event.id)">
            <text class="view-btn-text">查看详情</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const activeStatus = ref('all')

const statusTabs = [
  { label: '全部', value: 'all' },
  { label: '报名中', value: 'enrolling' },
  { label: '进行中', value: 'ongoing' },
  { label: '已结束', value: 'finished' },
]

const events = ref([
  {
    id: '1',
    title: '南京市掼蛋公开赛',
    date: '2024-06-01 09:00',
    location: '南京国际博览中心',
    prize: 10000,
    fee: 200,
    enrolled: 128,
    capacity: 256,
    status: 'enrolling',
    statusLabel: '报名中',
    statusClass: 'enrolling',
  },
  {
    id: '2',
    title: '长三角掼蛋省赛事',
    date: '2024-06-15 09:00',
    location: '上海某某酒店',
    prize: 20000,
    fee: 300,
    enrolled: 64,
    capacity: 128,
    status: 'enrolling',
    statusLabel: '报名中',
    statusClass: 'enrolling',
  },
  {
    id: '3',
    title: '企业家掼蛋交流赛',
    date: '2024-05-28 14:00',
    location: '高新掼蛋俱乐部3楼',
    prize: 5000,
    fee: 500,
    enrolled: 32,
    capacity: 32,
    status: 'ongoing',
    statusLabel: '进行中',
    statusClass: 'ongoing',
  },
  {
    id: '4',
    title: '春季友谊赛',
    date: '2024-05-10 09:00',
    location: '江宁文体中心',
    prize: 3000,
    fee: 100,
    enrolled: 64,
    capacity: 64,
    status: 'finished',
    statusLabel: '已结束',
    statusClass: 'finished',
  },
])

const filteredEvents = computed(() => {
  if (activeStatus.value === 'all') return events.value
  return events.value.filter(e => e.status === activeStatus.value)
})

function goDetail(id: string) {
  uni.navigateTo({ url: `/pages/events/detail?id=${id}` })
}

function handleEnroll(event: any) {
  uni.navigateTo({ url: `/pages/events/payment?id=${event.id}` })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding-bottom: 120rpx;
}

/* 顶部标签 */
.top-tabs {
  display: flex;
  background-color: #FFFFFF;
  padding: 16rpx 24rpx;
  gap: 24rpx;
  border-bottom: 1rpx solid #F0F0F0;
}

.top-tab {
  padding: 8rpx 0;
}

.top-tab.active {
  border-bottom: 4rpx solid #C41E3A;
}

.top-tab-text {
  font-size: 28rpx;
  color: #999999;
}

.top-tab-text.active {
  color: #C41E3A;
  font-weight: 600;
}

/* 赛事列表 */
.event-scroll {
  height: calc(100vh - 120rpx);
  padding: 16rpx 24rpx;
}

.event-card {
  background-color: #FFFFFF;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.event-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.event-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #333333;
  flex: 1;
  margin-right: 16rpx;
}

.event-status {
  padding: 4rpx 16rpx;
  border-radius: 6rpx;
  flex-shrink: 0;
}

.event-status.enrolling {
  background-color: #E8F5E9;
}

.event-status.ongoing {
  background-color: #E3F2FD;
}

.event-status.finished {
  background-color: #F5F5F5;
}

.status-text {
  font-size: 22rpx;
  color: #4CAF50;
}

.event-status.ongoing .status-text {
  color: #2196F3;
}

.event-status.finished .status-text {
  color: #999999;
}

/* 赛事信息 */
.event-info-list {
  display: flex;
  flex-direction: column;
  gap: 10rpx;
  margin-bottom: 16rpx;
}

.event-info-row {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.info-icon {
  font-size: 24rpx;
}

.info-text {
  font-size: 26rpx;
  color: #666666;
}

/* 赛事底部 */
.event-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16rpx;
  border-top: 1rpx solid #F0F0F0;
}

.event-fee-info {
  display: flex;
  align-items: baseline;
  gap: 12rpx;
}

.event-fee {
  font-size: 32rpx;
  font-weight: 700;
  color: #C41E3A;
}

.event-capacity {
  font-size: 24rpx;
  color: #999999;
}

.enroll-btn {
  background-color: #C41E3A;
  border-radius: 24rpx;
  padding: 12rpx 32rpx;
}

.enroll-btn-text {
  font-size: 26rpx;
  color: #FFFFFF;
  font-weight: 500;
}

.view-btn {
  border: 1rpx solid #C41E3A;
  border-radius: 24rpx;
  padding: 12rpx 32rpx;
}

.view-btn-text {
  font-size: 26rpx;
  color: #C41E3A;
}
</style>
