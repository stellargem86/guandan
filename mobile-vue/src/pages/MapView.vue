<template>
  <div class="page map-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-back" @click="$router.back()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
        </div>
        <div class="header-title">掼蛋地图</div>
        <div class="header-right">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        </div>
      </div>
    </div>

    <!-- Map Area -->
    <div class="map-area">
      <div class="map-placeholder">
        <div class="map-grid">
          <div v-for="i in 12" :key="i" class="map-block" :style="{ opacity: 0.3 + Math.random() * 0.4 }"></div>
        </div>
        <!-- Map Pins -->
        <div class="map-pin pin-1">
          <svg width="24" height="32" viewBox="0 0 24 32"><path d="M12 0C5.4 0 0 5.4 0 12c0 9 12 20 12 20s12-11 12-20c0-6.6-5.4-12-12-12z" fill="#C62828"/><circle cx="12" cy="12" r="5" fill="white"/></svg>
        </div>
        <div class="map-pin pin-2">
          <svg width="24" height="32" viewBox="0 0 24 32"><path d="M12 0C5.4 0 0 5.4 0 12c0 9 12 20 12 20s12-11 12-20c0-6.6-5.4-12-12-12z" fill="#C62828"/><circle cx="12" cy="12" r="5" fill="white"/></svg>
        </div>
        <div class="map-pin pin-3">
          <svg width="24" height="32" viewBox="0 0 24 32"><path d="M12 0C5.4 0 0 5.4 0 12c0 9 12 20 12 20s12-11 12-20c0-6.6-5.4-12-12-12z" fill="#C62828"/><circle cx="12" cy="12" r="5" fill="white"/></svg>
        </div>
        <div class="map-pin pin-4">
          <svg width="20" height="28" viewBox="0 0 24 32"><path d="M12 0C5.4 0 0 5.4 0 12c0 9 12 20 12 20s12-11 12-20c0-6.6-5.4-12-12-12z" fill="#9B1B30" opacity="0.7"/><circle cx="12" cy="12" r="5" fill="white"/></svg>
        </div>
      </div>
    </div>

    <!-- Bottom Sheet -->
    <div class="bottom-sheet">
      <div class="sheet-handle"></div>
      <div class="sheet-header">
        <span class="sheet-title">附近牌场</span>
        <span class="sheet-count">共 {{ merchants.length }} 家</span>
      </div>

      <!-- Featured Card -->
      <div class="featured-card" @click="$router.push('/merchant/1')">
        <div class="featured-image">
          <div class="featured-placeholder">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
          </div>
          <div class="featured-badge">推荐</div>
        </div>
        <div class="featured-info">
          <h3 class="featured-name">同庆楼·掼蛋主题餐厅</h3>
          <div class="featured-rating">
            <div class="stars">
              <svg v-for="i in 5" :key="i" width="12" height="12" viewBox="0 0 24 24" fill="#FF9800"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          </div>
            <span class="rating-score">4.9</span>
            <span class="rating-count">(326评价)</span>
          </div>
          <div class="featured-details">
            <span class="detail-item">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
              距离 1.2km
            </span>
            <span class="detail-item">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              可容纳 12桌
            </span>
          </div>
          <div class="featured-price">
            <span class="price-value">¥128</span>
            <span class="price-unit">/人起</span>
          </div>
        </div>
      </div>

      <!-- Merchant List -->
      <div class="merchant-list">
        <div v-for="merchant in merchants" :key="merchant.id" class="merchant-item" @click="$router.push(`/merchant/${merchant.id}`)">
          <div class="merchant-thumb" :style="{ background: merchant.color }">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
          </div>
          <div class="merchant-info">
            <h4 class="merchant-name">{{ merchant.name }}</h4>
            <div class="merchant-tags">
              <span v-for="tag in merchant.tags" :key="tag" class="merchant-tag">{{ tag }}</span>
            </div>
            <div class="merchant-meta">
              <span class="meta-distance">{{ merchant.distance }}</span>
              <span class="meta-dot">·</span>
              <span class="meta-rating">{{ merchant.rating }}分</span>
            </div>
          </div>
          <div class="merchant-price">
            <span class="price-amount">¥{{ merchant.price }}</span>
            <span class="price-per">/人</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const merchants = [
  { id: 2, name: '金陵棋牌会所', tags: ['掼蛋', '麻将'], distance: '0.8km', rating: 4.7, price: 88, color: 'linear-gradient(135deg, #667eea, #764ba2)' },
  { id: 3, name: '紫金山茶馆·棋牌', tags: ['掼蛋', '茶歇'], distance: '1.5km', rating: 4.8, price: 158, color: 'linear-gradient(135deg, #f093fb, #f5576c)' },
  { id: 4, name: '秦淮河畔休闲中心', tags: ['掼蛋', '餐饮'], distance: '2.1km', rating: 4.6, price: 68, color: 'linear-gradient(135deg, #4facfe, #00f2fe)' },
  { id: 5, name: '鼓楼掼蛋精英会', tags: ['高端', '商务'], distance: '3.2km', rating: 4.9, price: 228, color: 'linear-gradient(135deg, #43e97b, #38f9d7)' },
]
</script>

<style scoped>
.map-page {
  background: var(--bg-page);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
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
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-area {
  height: 280px;
  position: relative;
  overflow: hidden;
}

.map-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, #e8f5e9, #c8e6c9);
  position: relative;
}

.map-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(3, 1fr);
  width: 100%;
  height: 100%;
  gap: 2px;
  padding: 2px;
}

.map-block {
  background: #a5d6a7;
  border-radius: 2px;
}

.map-pin {
  position: absolute;
}

.pin-1 { top: 30%; left: 25%; }
.pin-2 { top: 45%; left: 55%; }
.pin-3 { top: 60%; left: 35%; }
.pin-4 { top: 25%; left: 70%; }

.bottom-sheet {
  flex: 1;
  background: var(--bg-card);
  border-radius: 20px 20px 0 0;
  margin-top: -16px;
  padding: 12px var(--spacing-lg) var(--spacing-lg);
  position: relative;
  z-index: 10;
}

.sheet-handle {
  width: 36px;
  height: 4px;
  background: #ddd;
  border-radius: 2px;
  margin: 0 auto 16px;
}

.sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.sheet-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.sheet-count {
  font-size: 12px;
  color: var(--text-tertiary);
}

.featured-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  margin-bottom: 16px;
  border: 1px solid var(--border-lighter);
}

.featured-image {
  height: 140px;
  background: linear-gradient(135deg, #8B1A2B, #C62828);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.featured-placeholder {
  opacity: 0.5;
}

.featured-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: var(--color-primary);
  color: white;
  font-size: 11px;
  padding: 3px 8px;
  border-radius: var(--radius-full);
}

.featured-info {
  padding: 14px;
}

.featured-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.featured-rating {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 8px;
}

.stars {
  display: flex;
  gap: 1px;
}

.rating-score {
  font-size: 13px;
  font-weight: 600;
  color: #FF9800;
  margin-left: 4px;
}

.rating-count {
  font-size: 11px;
  color: var(--text-tertiary);
}

.featured-details {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
}

.featured-price {
  margin-top: 4px;
}

.price-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-price);
}

.price-unit {
  font-size: 12px;
  color: var(--text-tertiary);
}

.merchant-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.merchant-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
}

.merchant-thumb {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.merchant-info {
  flex: 1;
  min-width: 0;
}

.merchant-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.merchant-tags {
  display: flex;
  gap: 4px;
  margin-bottom: 4px;
}

.merchant-tag {
  font-size: 10px;
  padding: 2px 6px;
  background: #fff0f0;
  color: var(--color-primary);
  border-radius: var(--radius-full);
}

.merchant-meta {
  font-size: 11px;
  color: var(--text-tertiary);
}

.meta-dot {
  margin: 0 4px;
}

.merchant-price {
  text-align: right;
  flex-shrink: 0;
}

.price-amount {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-price);
}

.price-per {
  font-size: 11px;
  color: var(--text-tertiary);
}
</style>
