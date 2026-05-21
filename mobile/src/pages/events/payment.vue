<template>
  <view class="page">
    <!-- 倒计时 -->
    <view class="countdown-bar">
      <text class="countdown-text">剩余 29:58 内完成支付</text>
    </view>

    <!-- 赛事信息 -->
    <view class="event-info-card">
      <text class="event-title">南京市掼蛋公开赛</text>
      <text class="event-date">2024-06-01 08:00</text>
      <view class="event-detail-row">
        <text class="detail-label">报名费</text>
        <text class="detail-value red">¥200/人</text>
      </view>
    </view>

    <!-- 报名数量 -->
    <view class="section-card">
      <view class="quantity-row">
        <text class="quantity-label">报名数量</text>
        <view class="quantity-control">
          <view class="qty-btn" @tap="decreaseQty">
            <text class="qty-btn-text">-</text>
          </view>
          <text class="qty-value">{{ quantity }}</text>
          <view class="qty-btn" @tap="increaseQty">
            <text class="qty-btn-text">+</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 合计金额 -->
    <view class="section-card">
      <view class="total-row">
        <text class="total-label">合计金额</text>
        <text class="total-value">¥{{ totalAmount }}</text>
      </view>
    </view>

    <!-- 支付方式 -->
    <view class="section-card">
      <text class="section-title">支付方式</text>
      <view class="payment-options">
        <view class="payment-option" :class="{ active: payMethod === 'wechat' }" @tap="payMethod = 'wechat'">
          <text class="pay-icon">💚</text>
          <text class="pay-name">微信支付</text>
          <view class="pay-radio" :class="{ checked: payMethod === 'wechat' }"></view>
        </view>
        <view class="payment-option" :class="{ active: payMethod === 'alipay' }" @tap="payMethod = 'alipay'">
          <text class="pay-icon">💙</text>
          <text class="pay-name">支付宝</text>
          <view class="pay-radio" :class="{ checked: payMethod === 'alipay' }"></view>
        </view>
      </view>
    </view>

    <!-- 底部确认支付 -->
    <view class="bottom-bar">
      <view class="bottom-total">
        <text class="bottom-total-label">合计:</text>
        <text class="bottom-total-value">¥{{ totalAmount }}</text>
      </view>
      <view class="pay-btn" @tap="handlePay">
        <text class="pay-btn-text">立即支付 ¥{{ totalAmount }}</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const quantity = ref(1)
const payMethod = ref('wechat')
const unitPrice = 200

const totalAmount = computed(() => quantity.value * unitPrice)

function increaseQty() {
  if (quantity.value < 10) quantity.value++
}

function decreaseQty() {
  if (quantity.value > 1) quantity.value--
}

function handlePay() {
  uni.showToast({ title: '支付成功', icon: 'success' })
  setTimeout(() => {
    uni.navigateTo({ url: '/pages/common/payment-result?status=success' })
  }, 1500)
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding-bottom: 140rpx;
}

/* 倒计时 */
.countdown-bar {
  background-color: #FFF3E0;
  padding: 16rpx 24rpx;
  text-align: center;
}

.countdown-text {
  font-size: 26rpx;
  color: #FF6F00;
  font-weight: 500;
}

/* 赛事信息 */
.event-info-card {
  background-color: #FFFFFF;
  margin: 16rpx 24rpx;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.event-title {
  font-size: 32rpx;
  font-weight: 700;
  color: #333333;
  margin-bottom: 8rpx;
}

.event-date {
  font-size: 24rpx;
  color: #999999;
  margin-bottom: 16rpx;
}

.event-detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16rpx;
  border-top: 1rpx solid #F0F0F0;
}

.detail-label {
  font-size: 26rpx;
  color: #666666;
}

.detail-value {
  font-size: 30rpx;
  font-weight: 700;
}

.detail-value.red {
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
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 16rpx;
}

/* 数量选择 */
.quantity-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.quantity-label {
  font-size: 28rpx;
  color: #333333;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.qty-btn {
  width: 56rpx;
  height: 56rpx;
  border: 1rpx solid #E0E0E0;
  border-radius: 8rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qty-btn-text {
  font-size: 32rpx;
  color: #333333;
}

.qty-value {
  font-size: 32rpx;
  font-weight: 600;
  color: #333333;
  min-width: 40rpx;
  text-align: center;
}

/* 合计 */
.total-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.total-label {
  font-size: 28rpx;
  color: #333333;
}

.total-value {
  font-size: 36rpx;
  font-weight: 700;
  color: #C41E3A;
}

/* 支付方式 */
.payment-options {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.payment-option {
  display: flex;
  align-items: center;
  padding: 20rpx;
  border: 1rpx solid #F0F0F0;
  border-radius: 12rpx;
  gap: 16rpx;
}

.payment-option.active {
  border-color: #C41E3A;
  background-color: #FFF5F5;
}

.pay-icon {
  font-size: 36rpx;
}

.pay-name {
  flex: 1;
  font-size: 28rpx;
  color: #333333;
}

.pay-radio {
  width: 36rpx;
  height: 36rpx;
  border: 2rpx solid #E0E0E0;
  border-radius: 50%;
}

.pay-radio.checked {
  border-color: #C41E3A;
  background-color: #C41E3A;
  box-shadow: inset 0 0 0 6rpx #FFFFFF;
}

/* 底部 */
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

.bottom-total {
  display: flex;
  align-items: baseline;
  gap: 8rpx;
  margin-right: 24rpx;
}

.bottom-total-label {
  font-size: 26rpx;
  color: #666666;
}

.bottom-total-value {
  font-size: 36rpx;
  font-weight: 700;
  color: #C41E3A;
}

.pay-btn {
  flex: 1;
  background-color: #C41E3A;
  border-radius: 40rpx;
  padding: 24rpx;
  text-align: center;
}

.pay-btn-text {
  font-size: 30rpx;
  color: #FFFFFF;
  font-weight: 600;
}
</style>
