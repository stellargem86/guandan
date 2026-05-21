<template>
  <view class="page">
    <!-- 地图区域 -->
    <view class="map-area">
      <view class="map-placeholder">
        <view class="map-grid">
          <view class="grid-line" v-for="i in 8" :key="i"></view>
        </view>
        <!-- 模拟地图标记 -->
        <view class="map-pin" v-for="pin in mapPins" :key="pin.id" :style="{ left: pin.x, top: pin.y }">
          <text class="pin-icon">📍</text>
          <view class="pin-label">
            <text class="pin-text">{{ pin.name }}</text>
          </view>
        </view>
        <!-- 用户位置 -->
        <view class="user-location">
          <view class="user-dot"></view>
          <view class="user-pulse"></view>
        </view>
        <text class="map-hint">地图加载中...</text>
      </view>
    </view>

    <!-- 底部商户列表 -->
    <view class="bottom-sheet">
      <view class="sheet-handle">
        <view class="handle-bar"></view>
      </view>
      <view class="sheet-header">
        <text class="sheet-title">附近牌场</text>
        <text class="sheet-count">共 {{ merchants.length }} 家</text>
      </view>

      <scroll-view scroll-y class="merchant-list">
        <view class="merchant-item" v-for="m in merchants" :key="m.id" @tap="goDetail(m.id)">
          <view class="merchant-cover">
            <text class="cover-emoji">{{ m.emoji }}</text>
          </view>
          <view class="merchant-info">
            <text class="merchant-name">{{ m.name }}</text>
            <view class="merchant-meta">
              <text class="merchant-rating">⭐ {{ m.rating }}</text>
              <text class="merchant-distance">{{ m.distance }}</text>
              <text class="merchant-capacity">{{ m.capacity }}/人</text>
            </view>
            <text class="merchant-address">{{ m.address }}</text>
          </view>
          <view class="merchant-arrow">
            <text class="arrow-text">›</text>
          </view>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const mapPins = ref([
  { id: '1', name: '金陵棋牌', x: '25%', y: '30%' },
  { id: '2', name: '龙虎山茶馆', x: '60%', y: '25%' },
  { id: '3', name: '紫金阁', x: '45%', y: '55%' },
  { id: '4', name: '秦淮雅集', x: '70%', y: '60%' },
  { id: '5', name: '玄武会所', x: '35%', y: '70%' },
])

const merchants = ref([
  {
    id: '1',
    name: '金陵棋牌会所',
    emoji: '🏆',
    rating: '4.9',
    distance: '1.2km',
    capacity: '128',
    address: '建邺区奥体大街68号3楼',
  },
  {
    id: '2',
    name: '龙虎山茶馆·掼蛋专区',
    emoji: '🍵',
    rating: '4.8',
    distance: '2.0km',
    capacity: '64',
    address: '鼓楼区中山路188号',
  },
  {
    id: '3',
    name: '紫金阁精品牌室',
    emoji: '🎴',
    rating: '4.7',
    distance: '3.5km',
    capacity: '48',
    address: '玄武区珠江路92号5楼',
  },
  {
    id: '4',
    name: '秦淮雅集·商务牌室',
    emoji: '🏮',
    rating: '4.9',
    distance: '4.1km',
    capacity: '96',
    address: '秦淮区夫子庙贡院街12号',
  },
  {
    id: '5',
    name: '玄武湖畔掼蛋会所',
    emoji: '🌊',
    rating: '4.6',
    distance: '5.2km',
    capacity: '80',
    address: '玄武区玄武湖公园东门旁',
  },
])

function goDetail(id: string) {
  uni.navigateTo({ url: `/pages/index/merchant-detail?id=${id}` })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  display: flex;
  flex-direction: column;
}

.map-area {
  height: 50vh;
  position: relative;
}

.map-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, #1e1e32 0%, #232338 100%);
  position: relative;
  overflow: hidden;
}

.map-grid {
  position: absolute;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.grid-line {
  height: 1rpx;
  background-color: rgba(58, 58, 80, 0.5);
}

.map-pin {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  transform: translate(-50%, -100%);
}

.pin-icon {
  font-size: 40rpx;
}

.pin-label {
  background-color: rgba(42, 42, 62, 0.9);
  border-radius: 8rpx;
  padding: 4rpx 12rpx;
  margin-top: 4rpx;
}

.pin-text {
  font-size: 18rpx;
  color: #f6c342;
  white-space: nowrap;
}

.user-location {
  position: absolute;
  left: 50%;
  top: 45%;
  transform: translate(-50%, -50%);
}

.user-dot {
  width: 24rpx;
  height: 24rpx;
  background-color: #3b82f6;
  border-radius: 50%;
  border: 4rpx solid #fff;
}

.user-pulse {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background-color: rgba(59, 130, 246, 0.2);
}

.map-hint {
  position: absolute;
  bottom: 20rpx;
  left: 50%;
  transform: translateX(-50%);
  font-size: 22rpx;
  color: #6b6b80;
}

/* 底部面板 */
.bottom-sheet {
  flex: 1;
  background-color: #1a1a2e;
  border-top-left-radius: 32rpx;
  border-top-right-radius: 32rpx;
  margin-top: -32rpx;
  position: relative;
  z-index: 10;
  padding: 0 32rpx;
}

.sheet-handle {
  display: flex;
  justify-content: center;
  padding: 20rpx 0;
}

.handle-bar {
  width: 64rpx;
  height: 8rpx;
  background-color: #3a3a50;
  border-radius: 4rpx;
}

.sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.sheet-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #f5f5f5;
}

.sheet-count {
  font-size: 24rpx;
  color: #6b6b80;
}

.merchant-list {
  height: 45vh;
}

.merchant-item {
  display: flex;
  align-items: center;
  padding: 24rpx;
  background-color: #2a2a3e;
  border-radius: 20rpx;
  margin-bottom: 16rpx;
}

.merchant-cover {
  width: 100rpx;
  height: 100rpx;
  background: linear-gradient(135deg, #32324a 0%, #2a2a3e 100%);
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
  border: 1rpx solid #3a3a50;
}

.cover-emoji {
  font-size: 44rpx;
}

.merchant-info {
  flex: 1;
}

.merchant-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: 8rpx;
}

.merchant-meta {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 6rpx;
}

.merchant-rating {
  font-size: 22rpx;
  color: #f6c342;
}

.merchant-distance {
  font-size: 22rpx;
  color: #6b6b80;
}

.merchant-capacity {
  font-size: 22rpx;
  color: #b0b0c0;
}

.merchant-address {
  font-size: 22rpx;
  color: #6b6b80;
}

.merchant-arrow {
  padding-left: 12rpx;
}

.arrow-text {
  font-size: 36rpx;
  color: #6b6b80;
}
</style>
