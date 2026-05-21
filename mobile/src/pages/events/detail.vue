<template>
  <view class="page">
    <!-- 赛事封面 -->
    <view class="cover-section">
      <view class="cover-bg">
        <text class="cover-title">南京市掼蛋公开赛</text>
        <text class="cover-sub">2024-06-01 09:00</text>
        <text class="cover-org">南京掼蛋博览中心</text>
      </view>
    </view>

    <!-- 报名信息卡片 -->
    <view class="enroll-card">
      <view class="enroll-row">
        <view class="enroll-item">
          <text class="enroll-label">报名费</text>
          <text class="enroll-value red">¥200/人</text>
        </view>
        <view class="enroll-item">
          <text class="enroll-label">已报名</text>
          <text class="enroll-value">128/256</text>
        </view>
      </view>
    </view>

    <!-- 比赛规则 -->
    <view class="section-card">
      <text class="section-title">比赛规则</text>
      <view class="rule-list">
        <text class="rule-text">采用国家体育总局掼蛋竞赛规则，小组赛循环，淘汰赛单败制。</text>
      </view>
    </view>

    <!-- 奖励设置 -->
    <view class="section-card">
      <text class="section-title">奖励设置</text>
      <view class="prize-list">
        <view class="prize-item">
          <view class="prize-icon gold">🥇</view>
          <text class="prize-label">冠军</text>
          <text class="prize-amount red">¥10000</text>
        </view>
        <view class="prize-item">
          <view class="prize-icon silver">🥈</view>
          <text class="prize-label">亚军</text>
          <text class="prize-amount red">¥5000</text>
        </view>
        <view class="prize-item">
          <view class="prize-icon bronze">🥉</view>
          <text class="prize-label">季军</text>
          <text class="prize-amount red">¥3000</text>
        </view>
      </view>
    </view>

    <!-- 底部报名 -->
    <view class="bottom-bar">
      <view class="bottom-fee">
        <text class="fee-label">报名费</text>
        <text class="fee-value">¥200/人</text>
      </view>
      <view class="bottom-enroll-btn" @tap="goPayment">
        <text class="bottom-enroll-text">立即报名</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
function goPayment() {
  uni.navigateTo({ url: '/pages/events/payment?id=1' })
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
  height: 360rpx;
  position: relative;
}

.cover-bg {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #8B0000 0%, #C41E3A 60%, #A01830 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
}

.cover-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #FFFFFF;
}

.cover-sub {
  font-size: 26rpx;
  color: rgba(255, 255, 255, 0.8);
}

.cover-org {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.6);
}

/* 报名信息 */
.enroll-card {
  background-color: #FFFFFF;
  margin: -32rpx 24rpx 16rpx;
  border-radius: 16rpx;
  padding: 24rpx;
  position: relative;
  z-index: 10;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
}

.enroll-row {
  display: flex;
  justify-content: space-around;
}

.enroll-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
}

.enroll-label {
  font-size: 24rpx;
  color: #999999;
}

.enroll-value {
  font-size: 32rpx;
  font-weight: 700;
  color: #333333;
}

.enroll-value.red {
  color: #C41E3A;
}

/* 通用区块 */
.section-card {
  background-color: #FFFFFF;
  margin: 16rpx 24rpx;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 16rpx;
}

.rule-list {
  padding: 0;
}

.rule-text {
  font-size: 26rpx;
  color: #666666;
  line-height: 1.8;
}

/* 奖励 */
.prize-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.prize-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 16rpx;
  background-color: #FFF8F0;
  border-radius: 12rpx;
}

.prize-icon {
  font-size: 36rpx;
}

.prize-label {
  flex: 1;
  font-size: 28rpx;
  font-weight: 500;
  color: #333333;
}

.prize-amount {
  font-size: 30rpx;
  font-weight: 700;
}

.prize-amount.red {
  color: #C41E3A;
}

/* 底部操作 */
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
}

.bottom-fee {
  display: flex;
  flex-direction: column;
  margin-right: 32rpx;
}

.fee-label {
  font-size: 22rpx;
  color: #999999;
}

.fee-value {
  font-size: 36rpx;
  font-weight: 700;
  color: #C41E3A;
}

.bottom-enroll-btn {
  flex: 1;
  background-color: #C41E3A;
  border-radius: 40rpx;
  padding: 24rpx;
  text-align: center;
}

.bottom-enroll-text {
  font-size: 30rpx;
  color: #FFFFFF;
  font-weight: 600;
}
</style>
