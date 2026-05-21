<template>
  <view class="page">
    <!-- 商户封面大图 -->
    <view class="cover-section">
      <view class="cover-bg">
        <text class="cover-text">同庆楼·掼蛋主题餐厅</text>
      </view>
      <view class="cover-tags">
        <view class="cover-tag">
          <text class="cover-tag-text">掼蛋</text>
        </view>
        <view class="cover-tag">
          <text class="cover-tag-text">棋牌</text>
        </view>
        <view class="cover-tag">
          <text class="cover-tag-text">聚会</text>
        </view>
      </view>
    </view>

    <!-- 商户基本信息 -->
    <view class="info-card">
      <view class="info-name-row">
        <text class="info-name">同庆楼·掼蛋主题餐厅</text>
        <view class="info-rating">
          <text class="rating-score">4.9</text>
          <text class="rating-stars">⭐⭐⭐⭐⭐</text>
        </view>
      </view>
      <view class="info-detail-list">
        <view class="info-row">
          <text class="info-icon">📍</text>
          <text class="info-text">南京市北武区中山路18号3层</text>
        </view>
        <view class="info-row">
          <text class="info-icon">🕐</text>
          <text class="info-text">10:00-24:00</text>
        </view>
        <view class="info-row">
          <text class="info-icon">📞</text>
          <text class="info-text">025-8888-6666</text>
        </view>
      </view>
    </view>

    <!-- 推荐套餐 -->
    <view class="section-card">
      <view class="card-header">
        <text class="card-title">推荐套餐</text>
      </view>
      <view class="package-list">
        <view class="package-item" v-for="pkg in packages" :key="pkg.id">
          <view class="package-info">
            <text class="package-name">{{ pkg.name }}</text>
            <text class="package-desc">{{ pkg.desc }}</text>
          </view>
          <view class="package-right">
            <text class="package-price">¥{{ pkg.price }}</text>
            <view class="package-buy-btn" @tap="handleBuy(pkg)">
              <text class="buy-text">立即购买</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 商户介绍 -->
    <view class="section-card">
      <view class="card-header">
        <text class="card-title">商户介绍</text>
      </view>
      <text class="desc-content">
        同庆楼·掼蛋主题餐厅位于南京市中心，是一家融合餐饮与掼蛋文化的特色场所。拥有20余间包厢，配备专业电子计分系统，提供高品质茶水服务。同时可承办企业团建、商务聚会、赛事活动等。
      </text>
    </view>

    <!-- 底部操作 -->
    <view class="bottom-bar">
      <view class="bottom-actions">
        <view class="bottom-icon-btn">
          <text class="bottom-icon">❤️</text>
          <text class="bottom-label">收藏</text>
        </view>
        <view class="bottom-icon-btn">
          <text class="bottom-icon">📞</text>
          <text class="bottom-label">电话</text>
        </view>
      </view>
      <view class="bottom-main-btn" @tap="handleBooking">
        <text class="bottom-main-text">立即预订</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const packages = ref([
  { id: '1', name: '商务入座套餐', desc: '含4小时牌桌+茶水+水果', price: 128 },
  { id: '2', name: '商务入座套餐', desc: '含VIP包间+茶歇+专属服务', price: 288 },
  { id: '3', name: '尊享聚会套餐', desc: '含包间+晚餐+酒水+管家服务', price: 488 },
])

function handleBuy(pkg: any) {
  uni.navigateTo({ url: `/pages/index/package-detail?id=${pkg.id}` })
}

function handleBooking() {
  uni.showToast({ title: '正在跳转预订...', icon: 'none' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding-bottom: 140rpx;
}

/* 封面 */
.cover-section {
  height: 400rpx;
  position: relative;
  background: linear-gradient(135deg, #8B2500 0%, #C41E3A 50%, #A01830 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-text {
  font-size: 36rpx;
  font-weight: 700;
  color: #FFFFFF;
}

.cover-tags {
  position: absolute;
  bottom: 24rpx;
  left: 24rpx;
  display: flex;
  gap: 12rpx;
}

.cover-tag {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20rpx;
  padding: 6rpx 16rpx;
}

.cover-tag-text {
  font-size: 22rpx;
  color: #FFFFFF;
}

/* 基本信息卡片 */
.info-card {
  background-color: #FFFFFF;
  margin: -32rpx 24rpx 16rpx;
  border-radius: 16rpx;
  padding: 24rpx;
  position: relative;
  z-index: 10;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
}

.info-name-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.info-name {
  font-size: 32rpx;
  font-weight: 700;
  color: #333333;
}

.info-rating {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.rating-score {
  font-size: 30rpx;
  font-weight: 700;
  color: #FF9800;
}

.rating-stars {
  font-size: 20rpx;
}

.info-detail-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.info-icon {
  font-size: 26rpx;
}

.info-text {
  font-size: 26rpx;
  color: #666666;
}

/* 通用section卡片 */
.section-card {
  background-color: #FFFFFF;
  margin: 16rpx 24rpx;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.card-header {
  margin-bottom: 16rpx;
}

.card-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #333333;
}

/* 套餐列表 */
.package-list {
  display: flex;
  flex-direction: column;
}

.package-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #F0F0F0;
}

.package-item:last-child {
  border-bottom: none;
}

.package-info {
  flex: 1;
}

.package-name {
  font-size: 28rpx;
  font-weight: 500;
  color: #333333;
  margin-bottom: 6rpx;
}

.package-desc {
  font-size: 24rpx;
  color: #999999;
}

.package-right {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.package-price {
  font-size: 32rpx;
  font-weight: 700;
  color: #C41E3A;
}

.package-buy-btn {
  background-color: #C41E3A;
  border-radius: 20rpx;
  padding: 10rpx 20rpx;
}

.buy-text {
  font-size: 22rpx;
  color: #FFFFFF;
}

/* 商户介绍 */
.desc-content {
  font-size: 26rpx;
  color: #666666;
  line-height: 1.8;
}

/* 底部操作栏 */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  padding: 20rpx 24rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  background-color: #FFFFFF;
  border-top: 1rpx solid #F0F0F0;
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.05);
}

.bottom-actions {
  display: flex;
  gap: 32rpx;
  margin-right: 24rpx;
}

.bottom-icon-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rpx;
}

.bottom-icon {
  font-size: 36rpx;
}

.bottom-label {
  font-size: 20rpx;
  color: #999999;
}

.bottom-main-btn {
  flex: 1;
  background-color: #C41E3A;
  border-radius: 40rpx;
  padding: 24rpx;
  text-align: center;
}

.bottom-main-text {
  font-size: 30rpx;
  color: #FFFFFF;
  font-weight: 600;
}
</style>
