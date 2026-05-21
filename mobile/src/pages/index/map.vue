<template>
  <view class="page">
    <!-- 地图区域 -->
    <view class="map-area">
      <view class="map-placeholder">
        <!-- 模拟地图背景 -->
        <view class="map-bg">
          <image src="/static/demo/map-bg.png" class="map-img" mode="aspectFill" />
        </view>
        <!-- 地图标记 -->
        <view class="map-pin" v-for="pin in mapPins" :key="pin.id" :style="{ left: pin.x, top: pin.y }">
          <view class="pin-marker">
            <text class="pin-emoji">📍</text>
          </view>
          <view class="pin-popup" v-if="pin.showPopup">
            <text class="pin-name">{{ pin.name }}</text>
          </view>
        </view>
        <!-- 用户位置 -->
        <view class="user-pin" style="left: 50%; top: 45%;">
          <view class="user-dot"></view>
          <view class="user-ring"></view>
        </view>
      </view>
    </view>

    <!-- 底部商户列表 -->
    <view class="bottom-panel">
      <view class="panel-handle">
        <view class="handle-bar"></view>
      </view>

      <!-- 筛选栏 -->
      <view class="filter-bar">
        <view class="filter-item active">
          <text class="filter-text active">全部</text>
        </view>
        <view class="filter-item">
          <text class="filter-text">掼蛋</text>
        </view>
        <view class="filter-item">
          <text class="filter-text">棋牌</text>
        </view>
        <view class="filter-item">
          <text class="filter-text">茶馆</text>
        </view>
      </view>

      <!-- 商户列表 -->
      <scroll-view scroll-y class="merchant-scroll">
        <view class="merchant-card" v-for="m in merchants" :key="m.id" @tap="goMerchantDetail(m.id)">
          <image v-if="m.image" :src="m.image" class="merchant-img" mode="aspectFill" />
          <view v-else class="merchant-img merchant-img-placeholder">
            <text class="img-emoji">{{ m.emoji }}</text>
          </view>
          <view class="merchant-info">
            <view class="merchant-name-row">
              <text class="merchant-name">{{ m.name }}</text>
              <view class="merchant-tag" v-if="m.tag">
                <text class="merchant-tag-text">{{ m.tag }}</text>
              </view>
            </view>
            <view class="merchant-rating">
              <text class="rating-text">⭐ {{ m.rating }}</text>
              <text class="rating-count">{{ m.reviewCount }}条</text>
            </view>
            <view class="merchant-bottom">
              <text class="merchant-distance">{{ m.distance }}</text>
              <text class="merchant-price">¥{{ m.price }}/人</text>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const mapPins = ref([
  { id: '1', name: '同庆楼·掼蛋主题餐厅', x: '30%', y: '25%', showPopup: true },
  { id: '2', name: '龙虎山茶馆', x: '55%', y: '35%', showPopup: false },
  { id: '3', name: '紫金阁', x: '40%', y: '55%', showPopup: false },
  { id: '4', name: '秦淮雅集', x: '65%', y: '60%', showPopup: false },
  { id: '5', name: '老头记·掼蛋茶馆', x: '25%', y: '65%', showPopup: false },
])

const merchants = ref([
  {
    id: '1',
    name: '同庆楼·掼蛋主题餐厅',
    emoji: '🏮',
    image: '',
    tag: '人气榜',
    rating: '4.9',
    reviewCount: 286,
    distance: '1.2km',
    price: 128,
  },
  {
    id: '2',
    name: '龙虎山茶馆·掼蛋专区',
    emoji: '🍵',
    image: '',
    tag: '',
    rating: '4.8',
    reviewCount: 156,
    distance: '2.0km',
    price: 88,
  },
  {
    id: '3',
    name: '紫金传奇·精品会所',
    emoji: '🎴',
    image: '',
    tag: '',
    rating: '4.7',
    reviewCount: 98,
    distance: '3.5km',
    price: 168,
  },
  {
    id: '4',
    name: '老头记·掼蛋茶馆',
    emoji: '☕',
    image: '',
    tag: '',
    rating: '4.6',
    reviewCount: 67,
    distance: '4.1km',
    price: 58,
  },
])

function goMerchantDetail(id: string) {
  uni.navigateTo({ url: `/pages/index/merchant-detail?id=${id}` })
}
</script>

<style scoped>
.page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #F5F5F5;
}

/* 地图区域 */
.map-area {
  height: 50vh;
  position: relative;
  background-color: #E8E4DC;
}

.map-placeholder {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.map-bg {
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, #E8E4DC 0%, #D4CFC6 100%);
}

.map-img {
  width: 100%;
  height: 100%;
}

.map-pin {
  position: absolute;
  transform: translate(-50%, -100%);
  z-index: 10;
}

.pin-marker {
  display: flex;
  align-items: center;
  justify-content: center;
}

.pin-emoji {
  font-size: 48rpx;
}

.pin-popup {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: #FFFFFF;
  border-radius: 8rpx;
  padding: 8rpx 16rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
  white-space: nowrap;
  margin-bottom: 8rpx;
}

.pin-name {
  font-size: 22rpx;
  color: #333333;
  font-weight: 500;
}

.user-pin {
  position: absolute;
  transform: translate(-50%, -50%);
  z-index: 5;
}

.user-dot {
  width: 24rpx;
  height: 24rpx;
  background-color: #2196F3;
  border-radius: 50%;
  border: 4rpx solid #FFFFFF;
  box-shadow: 0 2rpx 8rpx rgba(33, 150, 243, 0.4);
}

.user-ring {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 60rpx;
  height: 60rpx;
  border-radius: 50%;
  background-color: rgba(33, 150, 243, 0.15);
}

/* 底部面板 */
.bottom-panel {
  flex: 1;
  background-color: #FFFFFF;
  border-radius: 24rpx 24rpx 0 0;
  margin-top: -24rpx;
  position: relative;
  z-index: 20;
  display: flex;
  flex-direction: column;
}

.panel-handle {
  display: flex;
  justify-content: center;
  padding: 16rpx 0;
}

.handle-bar {
  width: 60rpx;
  height: 8rpx;
  background-color: #E0E0E0;
  border-radius: 4rpx;
}

.filter-bar {
  display: flex;
  padding: 8rpx 24rpx 16rpx;
  gap: 16rpx;
}

.filter-item {
  padding: 8rpx 24rpx;
  border-radius: 24rpx;
  background-color: #F5F5F5;
}

.filter-item.active {
  background-color: #C41E3A;
}

.filter-text {
  font-size: 24rpx;
  color: #666666;
}

.filter-text.active {
  color: #FFFFFF;
}

/* 商户列表 */
.merchant-scroll {
  flex: 1;
  padding: 0 24rpx;
}

.merchant-card {
  display: flex;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #F0F0F0;
}

.merchant-card:last-child {
  border-bottom: none;
}

.merchant-img {
  width: 160rpx;
  height: 120rpx;
  border-radius: 12rpx;
  margin-right: 20rpx;
  flex-shrink: 0;
}

.merchant-img-placeholder {
  background-color: #FFF0F0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.img-emoji {
  font-size: 48rpx;
}

.merchant-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.merchant-name-row {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.merchant-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
}

.merchant-tag {
  background-color: #FFF0F0;
  border-radius: 4rpx;
  padding: 2rpx 8rpx;
}

.merchant-tag-text {
  font-size: 20rpx;
  color: #C41E3A;
}

.merchant-rating {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.rating-text {
  font-size: 24rpx;
  color: #FF9800;
}

.rating-count {
  font-size: 22rpx;
  color: #999999;
}

.merchant-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.merchant-distance {
  font-size: 22rpx;
  color: #999999;
}

.merchant-price {
  font-size: 28rpx;
  color: #C41E3A;
  font-weight: 600;
}
</style>
