<template>
  <div class="page payment-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-back" @click="$router.back()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
        </div>
        <div class="header-title">报名支付</div>
        <div class="header-right"></div>
      </div>
    </div>

    <!-- Countdown -->
    <div class="countdown-bar">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#C62828" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      <span>支付剩余时间</span>
      <span class="countdown-time">14:58</span>
    </div>

    <!-- Event Info -->
    <div class="section-card">
      <h3 class="card-title">赛事信息</h3>
      <div class="event-summary">
        <div class="event-thumb">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.5"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
        </div>
        <div class="event-info">
          <h4 class="event-name">2024南京市掼蛋精英邀请赛</h4>
          <p class="event-date">2024年3月15日 14:00</p>
          <p class="event-location">同庆楼·掼蛋主题餐厅 3楼</p>
        </div>
      </div>
    </div>

    <!-- Price & Quantity -->
    <div class="section-card">
      <h3 class="card-title">报名信息</h3>
      <div class="price-row">
        <span class="price-label">报名费</span>
        <span class="price-value">¥200/人</span>
      </div>
      <div class="quantity-row">
        <span class="quantity-label">报名人数</span>
        <div class="quantity-control">
          <button class="qty-btn" @click="qty > 1 && qty--">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/></svg>
          </button>
          <span class="qty-value">{{ qty }}</span>
          <button class="qty-btn" @click="qty++">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          </button>
        </div>
      </div>
      <div class="total-row">
        <span class="total-label">合计</span>
        <span class="total-value">¥{{ qty * 200 }}</span>
      </div>
    </div>

    <!-- Payment Method -->
    <div class="section-card">
      <h3 class="card-title">支付方式</h3>
      <div class="payment-methods">
        <label class="payment-method active">
          <div class="method-icon wechat">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M8.5 11a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zm5 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zM12 2C6.477 2 2 6.145 2 11.243c0 2.936 1.444 5.544 3.767 7.29L5 22l3.77-2.034A11.58 11.58 0 0 0 12 20.486c5.523 0 10-4.145 10-9.243S17.523 2 12 2z"/></svg>
          </div>
          <span class="method-name">微信支付</span>
          <div class="method-check">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="#C62828"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
          </div>
        </label>
        <label class="payment-method">
          <div class="method-icon alipay">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
          </div>
          <span class="method-name">支付宝</span>
          <div class="method-check"></div>
        </label>
      </div>
    </div>

    <!-- Bottom Action -->
    <div class="bottom-action">
      <button class="pay-btn">立即支付 ¥{{ qty * 200 }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const qty = ref(1)
</script>

<style scoped>
.payment-page {
  background: var(--bg-page);
  min-height: 100vh;
  padding-bottom: 80px;
}

.header {
  background: var(--gradient-header);
  padding: var(--safe-area-top) var(--spacing-lg) 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  height: var(--header-height);
  display: flex;
  align-items: center;
}

.header-back {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-title {
  flex: 1;
  text-align: center;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-white);
}

.header-right {
  width: 32px;
}

.countdown-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  background: #fff5f5;
  font-size: 13px;
  color: var(--text-secondary);
}

.countdown-time {
  font-weight: 700;
  color: var(--text-price);
  font-size: 16px;
}

.section-card {
  background: var(--bg-card);
  margin: 12px var(--spacing-lg);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-card);
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 14px;
}

.event-summary {
  display: flex;
  gap: 12px;
}

.event-thumb {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-sm);
  background: var(--gradient-header);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.event-info {
  flex: 1;
}

.event-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.event-date, .event-location {
  font-size: 12px;
  color: var(--text-tertiary);
  line-height: 1.6;
}

.price-row, .quantity-row, .total-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
}

.price-row {
  border-bottom: 1px solid var(--border-lighter);
}

.quantity-row {
  border-bottom: 1px solid var(--border-lighter);
}

.price-label, .quantity-label, .total-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.price-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 16px;
}

.qty-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  color: var(--text-secondary);
}

.qty-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  min-width: 20px;
  text-align: center;
}

.total-label {
  font-weight: 500;
}

.total-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-price);
}

.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.payment-method {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-light);
  cursor: pointer;
}

.payment-method.active {
  border-color: var(--color-primary);
  background: #fff8f8;
}

.method-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.method-icon.wechat {
  background: #07C160;
}

.method-icon.alipay {
  background: #1677FF;
}

.method-name {
  flex: 1;
  font-size: 14px;
  color: var(--text-primary);
}

.bottom-action {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  padding: 12px var(--spacing-lg);
  background: var(--bg-card);
  border-top: 1px solid var(--border-light);
}

.pay-btn {
  width: 100%;
  height: 48px;
  background: var(--gradient-button);
  color: white;
  border-radius: var(--radius-full);
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(198, 40, 40, 0.3);
}
</style>
