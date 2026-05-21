<template>
  <div class="page merchant-detail-page">
    <!-- Photo Area -->
    <div class="photo-area">
      <div class="photo-placeholder">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
      </div>
      <div class="photo-back" @click="$router.back()">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
      </div>
      <div class="photo-indicators">
        <span class="indicator active"></span>
        <span class="indicator"></span>
        <span class="indicator"></span>
        <span class="indicator"></span>
      </div>
    </div>

    <!-- Info Card -->
    <div class="info-card">
      <h1 class="merchant-name">同庆楼·掼蛋主题餐厅</h1>
      <div class="merchant-rating">
        <div class="stars-row">
          <svg v-for="i in 5" :key="i" width="14" height="14" viewBox="0 0 24 24" fill="#FF9800"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
        </div>
        <span class="rating-text">4.9分</span>
        <span class="review-count">326条评价</span>
      </div>
      <div class="merchant-details">
        <div class="detail-row">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          <span>南京市鼓楼区中山北路178号</span>
        </div>
        <div class="detail-row">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <span>营业时间：10:00 - 23:00</span>
        </div>
        <div class="detail-row">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72"/></svg>
          <span>025-8888-6666</span>
        </div>
      </div>
      <div class="merchant-tags">
        <span class="tag">掼蛋</span>
        <span class="tag">商务</span>
        <span class="tag">餐饮</span>
        <span class="tag">包厢</span>
        <span class="tag">停车场</span>
      </div>
    </div>

    <!-- Packages Section -->
    <div class="section">
      <div class="section-header">
        <span class="section-title">推荐套餐</span>
      </div>
      <div class="package-list">
        <div v-for="pkg in packages" :key="pkg.id" class="package-card">
          <div class="package-info">
            <h3 class="package-name">{{ pkg.name }}</h3>
            <p class="package-desc">{{ pkg.desc }}</p>
            <div class="package-includes">
              <span v-for="item in pkg.includes" :key="item" class="include-item">{{ item }}</span>
            </div>
          </div>
          <div class="package-action">
            <div class="package-price">
              <span class="price-value">¥{{ pkg.price }}</span>
              <span class="price-unit">{{ pkg.unit }}</span>
            </div>
            <button class="book-btn">立即预订</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Action -->
    <div class="bottom-action">
      <button class="action-call">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72"/></svg>
        电话咨询
      </button>
      <button class="action-book">立即预订</button>
    </div>
  </div>
</template>

<script setup lang="ts">
const packages = [
  {
    id: 1,
    name: '商务组局套餐',
    desc: '适合商务宴请，含专属包厢和茶歇服务',
    price: 128,
    unit: '/人',
    includes: ['专属包厢', '茶歇服务', '掼蛋牌具', '停车位']
  },
  {
    id: 2,
    name: '朋友聚会套餐',
    desc: '轻松愉快的掼蛋局，含小食饮品',
    price: 88,
    unit: '/人',
    includes: ['大厅卡座', '饮品小食', '掼蛋牌具']
  },
  {
    id: 3,
    name: '精品VIP套餐',
    desc: '顶级私密空间，专属管家服务',
    price: 288,
    unit: '/人',
    includes: ['VIP包厢', '定制餐饮', '管家服务', '代客泊车', '纪念礼品']
  },
]
</script>

<style scoped>
.merchant-detail-page {
  background: var(--bg-page);
  min-height: 100vh;
  padding-bottom: 80px;
}

.photo-area {
  height: 240px;
  background: linear-gradient(135deg, #5c3d2e, #8d5a3c);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-back {
  position: absolute;
  top: calc(var(--safe-area-top) + 8px);
  left: 16px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-indicators {
  position: absolute;
  bottom: 16px;
  display: flex;
  gap: 6px;
}

.indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
}

.indicator.active {
  width: 18px;
  border-radius: 3px;
  background: white;
}

.info-card {
  background: var(--bg-card);
  margin: -20px var(--spacing-lg) 12px;
  border-radius: var(--radius-md);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-card);
  position: relative;
  z-index: 10;
}

.merchant-name {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.merchant-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.stars-row {
  display: flex;
  gap: 1px;
}

.rating-text {
  font-size: 14px;
  font-weight: 600;
  color: #FF9800;
}

.review-count {
  font-size: 12px;
  color: var(--text-tertiary);
}

.merchant-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
}

.merchant-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  font-size: 11px;
  padding: 4px 10px;
  background: #fff0f0;
  color: var(--color-primary);
  border-radius: var(--radius-full);
}

.section {
  padding: 0 var(--spacing-lg);
}

.section-header {
  margin-bottom: 12px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.package-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.package-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-card);
}

.package-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.package-desc {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.package-includes {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}

.include-item {
  font-size: 11px;
  padding: 2px 8px;
  background: #f5f5f5;
  color: var(--text-secondary);
  border-radius: var(--radius-full);
}

.package-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid var(--border-lighter);
}

.package-price .price-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-price);
}

.package-price .price-unit {
  font-size: 12px;
  color: var(--text-tertiary);
}

.book-btn {
  padding: 8px 20px;
  background: var(--gradient-button);
  color: white;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 500;
}

.bottom-action {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  display: flex;
  gap: 12px;
  padding: 12px var(--spacing-lg);
  background: var(--bg-card);
  border-top: 1px solid var(--border-light);
}

.action-call {
  flex: 1;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 500;
  background: white;
}

.action-book {
  flex: 2;
  height: 44px;
  background: var(--gradient-button);
  color: white;
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 600;
}
</style>
