<template>
  <view class="page">
    <view class="login-container">
      <!-- Logo区域 -->
      <view class="logo-section">
        <view class="logo-circle">
          <text class="logo-emoji">🃏</text>
        </view>
        <text class="app-name">深掼会</text>
        <text class="app-tagline">同城掼蛋 · 约局交友 · 商务社交</text>
      </view>

      <!-- 特色描述 -->
      <view class="features">
        <view class="feature-item">
          <text class="feature-icon">🎯</text>
          <text class="feature-text">ELO段位匹配</text>
        </view>
        <view class="feature-item">
          <text class="feature-icon">🏆</text>
          <text class="feature-text">官方认证赛事</text>
        </view>
        <view class="feature-item">
          <text class="feature-icon">🤝</text>
          <text class="feature-text">商务精英圈</text>
        </view>
      </view>

      <!-- 登录按钮 -->
      <view class="login-section">
        <view class="wechat-btn" @tap="handleWechatLogin">
          <text class="wechat-icon">💬</text>
          <text class="wechat-text">微信一键登录</text>
        </view>

        <view class="phone-btn" @tap="handlePhoneLogin">
          <text class="phone-text">手机号登录</text>
        </view>
      </view>

      <!-- 用户协议 -->
      <view class="agreement-section">
        <view class="checkbox-wrap" @tap="toggleAgreement">
          <view class="checkbox" :class="{ checked: agreed }">
            <text class="check-mark" v-if="agreed">✓</text>
          </view>
        </view>
        <text class="agreement-text">
          我已阅读并同意
          <text class="agreement-link">《用户服务协议》</text>
          和
          <text class="agreement-link">《隐私政策》</text>
        </text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const agreed = ref(false)

function toggleAgreement() {
  agreed.value = !agreed.value
}

function handleWechatLogin() {
  if (!agreed.value) {
    uni.showToast({ title: '请先同意用户协议', icon: 'none' })
    return
  }
  uni.showToast({ title: '登录成功', icon: 'success' })
  setTimeout(() => {
    uni.switchTab({ url: '/pages/index/index' })
  }, 1500)
}

function handlePhoneLogin() {
  if (!agreed.value) {
    uni.showToast({ title: '请先同意用户协议', icon: 'none' })
    return
  }
  uni.showToast({ title: '手机号登录功能即将开放', icon: 'none' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
}

.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 64rpx 48rpx;
}

/* Logo */
.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 64rpx;
}

.logo-circle {
  width: 160rpx;
  height: 160rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 32rpx;
  box-shadow: 0 8px 32px rgba(246, 195, 66, 0.3);
}

.logo-emoji {
  font-size: 80rpx;
}

.app-name {
  font-size: 56rpx;
  font-weight: 800;
  color: #f5f5f5;
  margin-bottom: 12rpx;
}

.app-tagline {
  font-size: 26rpx;
  color: #6b6b80;
}

/* 特色 */
.features {
  display: flex;
  gap: 40rpx;
  margin-bottom: 80rpx;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
}

.feature-icon {
  font-size: 40rpx;
}

.feature-text {
  font-size: 22rpx;
  color: #b0b0c0;
}

/* 登录按钮 */
.login-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24rpx;
  margin-bottom: 48rpx;
}

.wechat-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 48rpx;
  padding: 32rpx;
  box-shadow: 0 4px 16px rgba(246, 195, 66, 0.25);
}

.wechat-icon {
  font-size: 36rpx;
}

.wechat-text {
  font-size: 32rpx;
  color: #1a1a2e;
  font-weight: 700;
}

.phone-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1rpx solid rgba(246, 195, 66, 0.4);
  border-radius: 48rpx;
  padding: 32rpx;
}

.phone-text {
  font-size: 30rpx;
  color: #f6c342;
  font-weight: 500;
}

/* 协议 */
.agreement-section {
  display: flex;
  align-items: flex-start;
  gap: 12rpx;
  padding: 0 16rpx;
}

.checkbox-wrap {
  padding-top: 4rpx;
}

.checkbox {
  width: 32rpx;
  height: 32rpx;
  border: 2rpx solid #6b6b80;
  border-radius: 8rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox.checked {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-color: #f6c342;
}

.check-mark {
  font-size: 20rpx;
  color: #1a1a2e;
  font-weight: 700;
}

.agreement-text {
  font-size: 22rpx;
  color: #6b6b80;
  line-height: 1.5;
}

.agreement-link {
  color: #f6c342;
}
</style>
