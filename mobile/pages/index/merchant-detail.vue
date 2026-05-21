<template>
  <view class="page">
    <!-- 顶部封面 -->
    <view class="cover-section">
      <view class="cover-bg">
        <text class="cover-emoji">🏆</text>
      </view>
      <view class="cover-overlay">
        <view class="cover-badge">
          <text class="badge-text">人气商户</text>
        </view>
      </view>
    </view>

    <!-- 商户信息 -->
    <view class="info-section">
      <text class="merchant-name">{{ merchant.name }}</text>
      <view class="rating-row">
        <text class="rating-stars">⭐⭐⭐⭐⭐</text>
        <text class="rating-score">{{ merchant.rating }}</text>
        <text class="rating-count">{{ merchant.reviewCount }}条评价</text>
      </view>
      <view class="info-items">
        <view class="info-item">
          <text class="info-icon">📍</text>
          <text class="info-text">{{ merchant.address }}</text>
        </view>
        <view class="info-item">
          <text class="info-icon">🕐</text>
          <text class="info-text">{{ merchant.businessHours }}</text>
        </view>
        <view class="info-item">
          <text class="info-icon">📞</text>
          <text class="info-text">{{ merchant.phone }}</text>
        </view>
        <view class="info-item">
          <text class="info-icon">👥</text>
          <text class="info-text">可容纳 {{ merchant.capacity }} 人</text>
        </view>
      </view>
    </view>

    <!-- 设施标签 -->
    <view class="tags-section">
      <view class="tag" v-for="tag in merchant.tags" :key="tag">
        <text class="tag-text">{{ tag }}</text>
      </view>
    </view>

    <!-- 推荐套餐 -->
    <view class="section-header">
      <text class="section-title">推荐套餐</text>
    </view>

    <view class="packages-list">
      <view class="package-card" v-for="pkg in packages" :key="pkg.id">
        <view class="package-info">
          <text class="package-name">{{ pkg.name }}</text>
          <text class="package-desc">{{ pkg.description }}</text>
          <view class="package-price-row">
            <text class="package-price">¥{{ pkg.price }}</text>
            <text class="package-original">¥{{ pkg.originalPrice }}</text>
          </view>
        </view>
        <view class="package-action">
          <view class="buy-btn" @tap="handleBuy(pkg)">
            <text class="buy-btn-text">立即购买</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 商户介绍 -->
    <view class="section-header">
      <text class="section-title">商户介绍</text>
    </view>
    <view class="desc-section">
      <text class="desc-text">{{ merchant.description }}</text>
    </view>

    <!-- 底部操作 -->
    <view class="bottom-bar">
      <view class="bottom-left">
        <view class="bottom-icon-btn">
          <text class="bottom-icon">❤️</text>
          <text class="bottom-icon-label">收藏</text>
        </view>
        <view class="bottom-icon-btn">
          <text class="bottom-icon">📞</text>
          <text class="bottom-icon-label">电话</text>
        </view>
      </view>
      <view class="bottom-main-btn" @tap="handleNavigate">
        <text class="bottom-main-text">导航前往</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const merchant = ref({
  name: '金陵棋牌会所',
  rating: '4.9',
  reviewCount: 286,
  address: '南京市建邺区奥体大街68号3楼',
  businessHours: '营业时间 10:00-02:00',
  phone: '025-8888-6666',
  capacity: 128,
  tags: ['WiFi', '停车场', '包间', '茶水', '计分器', '空调', '禁烟区'],
  description: '金陵棋牌会所是南京地区最具人气的掼蛋专业场地，拥有30余张牌桌、8间VIP包间。会所配备专业电子计分系统、高清监控回放、舒适座椅及优质茶水服务。每周举办俱乐部赛事及段位赛，是深掼会认证合作商户。',
})

const packages = ref([
  {
    id: '1',
    name: '畅玩套餐',
    description: '含4小时牌桌+茶水+水果拼盘',
    price: 128,
    originalPrice: 168,
  },
  {
    id: '2',
    name: '商务包间套餐',
    description: '含VIP包间4小时+茶歇+点心+专属服务',
    price: 288,
    originalPrice: 388,
  },
  {
    id: '3',
    name: '尊享聚会套餐',
    description: '含VIP包间6小时+晚餐+酒水+专属管家',
    price: 488,
    originalPrice: 668,
  },
])

function handleBuy(pkg: any) {
  uni.showToast({ title: `已选择: ${pkg.name}`, icon: 'none' })
}

function handleNavigate() {
  uni.showToast({ title: '正在打开导航...', icon: 'none' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 160rpx;
}

.cover-section {
  position: relative;
  height: 360rpx;
}

.cover-bg {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #2a2a3e 0%, #32324a 50%, #1e1e32 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-emoji {
  font-size: 120rpx;
}

.cover-overlay {
  position: absolute;
  bottom: 20rpx;
  right: 24rpx;
}

.cover-badge {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 20rpx;
  padding: 8rpx 24rpx;
}

.badge-text {
  font-size: 22rpx;
  color: #1a1a2e;
  font-weight: 600;
}

/* 商户信息 */
.info-section {
  padding: 32rpx;
}

.merchant-name {
  font-size: 40rpx;
  font-weight: 700;
  color: #f5f5f5;
  margin-bottom: 16rpx;
}

.rating-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 24rpx;
}

.rating-stars {
  font-size: 24rpx;
}

.rating-score {
  font-size: 28rpx;
  color: #f6c342;
  font-weight: 600;
}

.rating-count {
  font-size: 24rpx;
  color: #6b6b80;
}

.info-items {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.info-icon {
  font-size: 28rpx;
}

.info-text {
  font-size: 26rpx;
  color: #b0b0c0;
}

/* 标签 */
.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  padding: 0 32rpx 32rpx;
}

.tag {
  background-color: rgba(246, 195, 66, 0.1);
  border: 1rpx solid rgba(246, 195, 66, 0.2);
  border-radius: 12rpx;
  padding: 8rpx 20rpx;
}

.tag-text {
  font-size: 22rpx;
  color: #f6c342;
}

/* 区域标题 */
.section-header {
  padding: 24rpx 32rpx 16rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #f5f5f5;
}

/* 套餐列表 */
.packages-list {
  padding: 0 32rpx;
}

.package-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #2a2a3e;
  border-radius: 20rpx;
  padding: 28rpx;
  margin-bottom: 16rpx;
}

.package-info {
  flex: 1;
}

.package-name {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: 8rpx;
}

.package-desc {
  font-size: 24rpx;
  color: #6b6b80;
  margin-bottom: 12rpx;
}

.package-price-row {
  display: flex;
  align-items: baseline;
  gap: 12rpx;
}

.package-price {
  font-size: 36rpx;
  font-weight: 700;
  color: #f6c342;
}

.package-original {
  font-size: 24rpx;
  color: #6b6b80;
  text-decoration: line-through;
}

.package-action {
  margin-left: 20rpx;
}

.buy-btn {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 16rpx;
  padding: 16rpx 28rpx;
}

.buy-btn-text {
  font-size: 24rpx;
  color: #1a1a2e;
  font-weight: 600;
  white-space: nowrap;
}

/* 介绍 */
.desc-section {
  padding: 0 32rpx 32rpx;
}

.desc-text {
  font-size: 26rpx;
  color: #b0b0c0;
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
  padding: 20rpx 32rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  background-color: #1a1a2e;
  border-top: 1rpx solid #3a3a50;
}

.bottom-left {
  display: flex;
  gap: 32rpx;
  margin-right: 32rpx;
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

.bottom-icon-label {
  font-size: 20rpx;
  color: #6b6b80;
}

.bottom-main-btn {
  flex: 1;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 16rpx;
  padding: 24rpx;
  text-align: center;
}

.bottom-main-text {
  font-size: 30rpx;
  color: #1a1a2e;
  font-weight: 700;
}
</style>
