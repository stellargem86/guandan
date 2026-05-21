<template>
  <div class="page event-detail-page">
    <!-- Banner -->
    <div class="banner">
      <div class="banner-back" @click="$router.back()">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
      </div>
    </div>

    <!-- Event Info Card -->
    <div class="info-card">
      <h1 class="event-title">2024南京市掼蛋精英邀请赛</h1>
      <div class="organizer">
        <div class="organizer-avatar">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </div>
        <span class="organizer-name">南京市掼蛋协会</span>
        <span class="organizer-badge">官方认证</span>
      </div>

      <!-- Key Metrics -->
      <div class="metrics">
        <div class="metric">
          <span class="metric-value">¥200</span>
          <span class="metric-label">报名费/人</span>
        </div>
        <div class="metric-divider"></div>
        <div class="metric">
          <span class="metric-value">96/128</span>
          <span class="metric-label">报名人数</span>
        </div>
        <div class="metric-divider"></div>
        <div class="metric">
          <span class="metric-value">¥10000</span>
          <span class="metric-label">奖金池</span>
        </div>
      </div>
    </div>

    <!-- Details Section -->
    <div class="section-card">
      <h3 class="section-title">赛事信息</h3>
      <div class="info-list">
        <div class="info-row">
          <span class="info-label">比赛时间</span>
          <span class="info-value">2024年3月15日 14:00-21:00</span>
        </div>
        <div class="info-row">
          <span class="info-label">比赛地点</span>
          <span class="info-value">同庆楼·掼蛋主题餐厅 3楼</span>
        </div>
        <div class="info-row">
          <span class="info-label">比赛形式</span>
          <span class="info-value">双人配对赛（瑞士制7轮）</span>
        </div>
        <div class="info-row">
          <span class="info-label">报名截止</span>
          <span class="info-value">2024年3月13日 18:00</span>
        </div>
      </div>
    </div>

    <!-- Rules Section -->
    <div class="section-card">
      <h3 class="section-title">比赛规则</h3>
      <div class="rules-content">
        <p>1. 采用国家体育总局掼蛋竞赛规则</p>
        <p>2. 每轮比赛限时45分钟，超时判负</p>
        <p>3. 禁止使用手势、暗号等作弊行为</p>
        <p>4. 裁判判罚为最终裁决</p>
        <p>5. 迟到15分钟视为弃权</p>
      </div>
    </div>

    <!-- Prize Section -->
    <div class="section-card">
      <h3 class="section-title">奖励设置</h3>
      <div class="prize-list">
        <div class="prize-item gold">
          <div class="prize-rank">
            <span class="rank-icon">🏆</span>
            <span class="rank-text">冠军</span>
          </div>
          <span class="prize-amount">¥10,000</span>
        </div>
        <div class="prize-item silver">
          <div class="prize-rank">
            <span class="rank-icon">🥈</span>
            <span class="rank-text">亚军</span>
          </div>
          <span class="prize-amount">¥5,000</span>
        </div>
        <div class="prize-item bronze">
          <div class="prize-rank">
            <span class="rank-icon">🥉</span>
            <span class="rank-text">季军</span>
          </div>
          <span class="prize-amount">¥2,000</span>
        </div>
        <div class="prize-item">
          <div class="prize-rank">
            <span class="rank-text">4-8名</span>
          </div>
          <span class="prize-amount">¥500</span>
        </div>
      </div>
    </div>

    <!-- Bottom Action -->
    <div class="bottom-action">
      <div class="action-info">
        <span class="action-price">¥200</span>
        <span class="action-unit">/人</span>
      </div>
      <button class="action-btn" @click="$router.push('/event/1/pay')">立即报名</button>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.event-detail-page {
  background: var(--bg-page);
  min-height: 100vh;
  padding-bottom: 80px;
}

.banner {
  height: 200px;
  background: linear-gradient(135deg, #6B0F1F, #9B1B30, #C62828);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.banner::after {
  content: '掼蛋精英赛';
  font-size: 24px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.2);
  letter-spacing: 4px;
}

.banner-back {
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

.info-card {
  background: var(--bg-card);
  margin: -24px var(--spacing-lg) 12px;
  border-radius: var(--radius-md);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-card);
  position: relative;
  z-index: 10;
}

.event-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 10px;
  line-height: 1.4;
}

.organizer {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.organizer-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--gradient-header);
  display: flex;
  align-items: center;
  justify-content: center;
}

.organizer-name {
  font-size: 13px;
  color: var(--text-secondary);
}

.organizer-badge {
  font-size: 10px;
  padding: 2px 6px;
  background: #fff0f0;
  color: var(--color-primary);
  border-radius: var(--radius-full);
}

.metrics {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 16px 0 0;
  border-top: 1px solid var(--border-lighter);
}

.metric {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.metric-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-price);
}

.metric-label {
  font-size: 11px;
  color: var(--text-tertiary);
}

.metric-divider {
  width: 1px;
  height: 30px;
  background: var(--border-lighter);
}

.section-card {
  background: var(--bg-card);
  margin: 0 var(--spacing-lg) 12px;
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-card);
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
  padding-left: 10px;
  border-left: 3px solid var(--color-primary);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-size: 13px;
  color: var(--text-tertiary);
}

.info-value {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 500;
}

.rules-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rules-content p {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.prize-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.prize-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-radius: var(--radius-sm);
  background: #fafafa;
}

.prize-item.gold {
  background: linear-gradient(135deg, #FFF8E1, #FFECB3);
}

.prize-item.silver {
  background: linear-gradient(135deg, #FAFAFA, #EEEEEE);
}

.prize-item.bronze {
  background: linear-gradient(135deg, #FBE9E7, #FFCCBC);
}

.prize-rank {
  display: flex;
  align-items: center;
  gap: 6px;
}

.rank-icon {
  font-size: 18px;
}

.rank-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.prize-amount {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-price);
}

.bottom-action {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px var(--spacing-lg);
  background: var(--bg-card);
  border-top: 1px solid var(--border-light);
}

.action-info {
  display: flex;
  align-items: baseline;
}

.action-price {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-price);
}

.action-unit {
  font-size: 12px;
  color: var(--text-tertiary);
}

.action-btn {
  padding: 12px 40px;
  background: var(--gradient-button);
  color: white;
  border-radius: var(--radius-full);
  font-size: 15px;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(198, 40, 40, 0.3);
}
</style>
