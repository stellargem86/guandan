<template>
  <view class="page">
    <!-- 余额卡片 -->
    <view class="balance-card">
      <text class="balance-label">账户余额（元）</text>
      <text class="balance-amount">680.00</text>
      <view class="balance-actions">
        <view class="balance-btn recharge" @tap="handleRecharge">
          <text class="balance-btn-text">充值</text>
        </view>
        <view class="balance-btn withdraw" @tap="handleWithdraw">
          <text class="balance-btn-text withdraw-text">提现</text>
        </view>
      </view>
    </view>

    <!-- 快捷金额 -->
    <view class="quick-amounts">
      <view
        class="amount-item"
        :class="{ active: selectedAmount === amount }"
        v-for="amount in quickAmounts"
        :key="amount"
        @tap="selectedAmount = amount"
      >
        <text class="amount-text" :class="{ active: selectedAmount === amount }">¥{{ amount }}</text>
      </view>
    </view>

    <!-- 交易记录 -->
    <view class="section-header">
      <text class="section-title">交易记录</text>
    </view>

    <scroll-view scroll-y class="transaction-list">
      <view class="transaction-item" v-for="tx in transactions" :key="tx.id">
        <view class="tx-left">
          <view class="tx-icon-wrap" :class="tx.type">
            <text class="tx-icon">{{ tx.icon }}</text>
          </view>
          <view class="tx-info">
            <text class="tx-desc">{{ tx.description }}</text>
            <text class="tx-date">{{ tx.date }}</text>
          </view>
        </view>
        <text class="tx-amount" :class="tx.type">{{ tx.amount }}</text>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const selectedAmount = ref(100)
const quickAmounts = [50, 100, 200, 500]

const transactions = ref([
  { id: '1', icon: '🏆', description: '赛事报名 - 城市精英赛', date: '2024-03-05 14:30', amount: '-200.00', type: 'expense' },
  { id: '2', icon: '💰', description: '充值', date: '2024-03-03 10:00', amount: '+500.00', type: 'income' },
  { id: '3', icon: '🎴', description: '套餐购买 - 畅玩套餐', date: '2024-03-01 20:15', amount: '-128.00', type: 'expense' },
  { id: '4', icon: '🏅', description: '赛事奖金 - 月度积分赛', date: '2024-02-28 18:00', amount: '+300.00', type: 'income' },
  { id: '5', icon: '💰', description: '押金退还 - 商务精英局', date: '2024-02-25 22:30', amount: '+100.00', type: 'income' },
  { id: '6', icon: '🎯', description: '组局押金 - 高段位竞技', date: '2024-02-25 19:00', amount: '-100.00', type: 'expense' },
  { id: '7', icon: '🏆', description: '赛事报名 - 月度积分赛', date: '2024-02-20 09:00', amount: '-50.00', type: 'expense' },
  { id: '8', icon: '💰', description: '充值', date: '2024-02-15 12:00', amount: '+200.00', type: 'income' },
])

function handleRecharge() {
  uni.showToast({ title: '充值功能开发中', icon: 'none' })
}

function handleWithdraw() {
  uni.showToast({ title: '提现功能开发中', icon: 'none' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
}

/* 余额卡片 */
.balance-card {
  margin: 32rpx;
  padding: 40rpx 32rpx;
  background: linear-gradient(135deg, #2a2a3e 0%, #32324a 100%);
  border-radius: 24rpx;
  border: 1rpx solid rgba(246, 195, 66, 0.1);
}

.balance-label {
  font-size: 26rpx;
  color: #6b6b80;
  margin-bottom: 12rpx;
  display: block;
}

.balance-amount {
  font-size: 64rpx;
  font-weight: 800;
  color: #f6c342;
  margin-bottom: 32rpx;
  display: block;
}

.balance-actions {
  display: flex;
  gap: 20rpx;
}

.balance-btn {
  flex: 1;
  padding: 22rpx;
  border-radius: 16rpx;
  text-align: center;
}

.balance-btn.recharge {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
}

.balance-btn.withdraw {
  border: 1rpx solid rgba(246, 195, 66, 0.4);
  background-color: transparent;
}

.balance-btn-text {
  font-size: 28rpx;
  color: #1a1a2e;
  font-weight: 600;
}

.withdraw-text {
  color: #f6c342;
}

/* 快捷金额 */
.quick-amounts {
  display: flex;
  gap: 16rpx;
  padding: 0 32rpx 32rpx;
}

.amount-item {
  flex: 1;
  padding: 20rpx;
  background-color: #2a2a3e;
  border-radius: 12rpx;
  text-align: center;
  border: 1rpx solid #3a3a50;
}

.amount-item.active {
  border-color: #f6c342;
  background-color: rgba(246, 195, 66, 0.08);
}

.amount-text {
  font-size: 26rpx;
  color: #b0b0c0;
}

.amount-text.active {
  color: #f6c342;
  font-weight: 600;
}

/* 交易记录 */
.section-header {
  padding: 16rpx 32rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
}

.transaction-list {
  padding: 0 32rpx;
  height: calc(100vh - 520rpx);
}

.transaction-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  margin-bottom: 12rpx;
}

.tx-left {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.tx-icon-wrap {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tx-icon-wrap.income {
  background-color: rgba(16, 185, 129, 0.12);
}

.tx-icon-wrap.expense {
  background-color: rgba(239, 68, 68, 0.12);
}

.tx-icon {
  font-size: 28rpx;
}

.tx-info {
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.tx-desc {
  font-size: 26rpx;
  color: #f5f5f5;
}

.tx-date {
  font-size: 22rpx;
  color: #6b6b80;
}

.tx-amount {
  font-size: 28rpx;
  font-weight: 600;
}

.tx-amount.income {
  color: #10b981;
}

.tx-amount.expense {
  color: #ef4444;
}
</style>
