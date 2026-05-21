<template>
  <div class="page club-detail-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-back" @click="$router.back()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
        </div>
        <div class="header-title">俱乐部详情</div>
        <div class="header-right">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
        </div>
      </div>
    </div>

    <!-- Club Header -->
    <div class="club-header">
      <div class="club-logo">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5"><path d="M12 2L4 7v6c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V7l-8-5z"/></svg>
      </div>
      <h1 class="club-name">金陵掼蛋俱乐部</h1>
      <p class="club-id">ID: GDC-NJ-001</p>
      <div class="club-badges">
        <span class="badge badge-verified">官方认证</span>
        <span class="badge badge-level">Lv.5</span>
      </div>
    </div>

    <!-- Tab Row -->
    <div class="tab-row">
      <div
        v-for="tab in tabs"
        :key="tab"
        class="tab-item"
        :class="{ active: activeTab === tab }"
        @click="activeTab = tab"
      >{{ tab }}</div>
    </div>

    <!-- Stats Row -->
    <div class="stats-card">
      <div class="stat-item">
        <span class="stat-value">128</span>
        <span class="stat-label">成员</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <span class="stat-value">36</span>
        <span class="stat-label">活动</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <span class="stat-value">4.9</span>
        <span class="stat-label">评分</span>
      </div>
      <div class="stat-divider"></div>
      <div class="stat-item">
        <span class="stat-value">82%</span>
        <span class="stat-label">活跃率</span>
      </div>
    </div>

    <!-- Club Intro -->
    <div class="section-card">
      <h3 class="section-title">俱乐部简介</h3>
      <p class="intro-text">
        金陵掼蛋俱乐部成立于2020年，是南京地区最具影响力的掼蛋竞技俱乐部之一。俱乐部定期举办各类掼蛋赛事，为会员提供专业的竞技训练和交流平台。我们致力于推广掼蛋文化，打造高品质的掼蛋社交圈。
      </p>
    </div>

    <!-- Recent Activities -->
    <div class="section-card">
      <h3 class="section-title">近期活动</h3>
      <div class="activity-list">
        <div v-for="activity in activities" :key="activity.id" class="activity-item">
          <div class="activity-date">
            <span class="date-day">{{ activity.day }}</span>
            <span class="date-month">{{ activity.month }}</span>
          </div>
          <div class="activity-info">
            <h4 class="activity-name">{{ activity.name }}</h4>
            <p class="activity-desc">{{ activity.desc }}</p>
          </div>
          <span class="activity-status" :class="activity.statusClass">{{ activity.status }}</span>
        </div>
      </div>
    </div>

    <!-- Bottom Action -->
    <div class="bottom-action">
      <button class="chat-btn" @click="$router.push('/club/1/chat')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        俱乐部聊天
      </button>
      <button class="join-btn">申请加入</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('公告')
const tabs = ['公告', '活动', '成绩', '聊天']

const activities = [
  { id: 1, day: '15', month: '3月', name: '周末友谊赛', desc: '面向全体会员的休闲掼蛋赛', status: '报名中', statusClass: 'status-open' },
  { id: 2, day: '20', month: '3月', name: '精英挑战赛', desc: '高级会员专属竞技赛事', status: '即将开始', statusClass: 'status-soon' },
  { id: 3, day: '25', month: '3月', name: '新手训练营', desc: '新会员掼蛋技巧培训', status: '已满员', statusClass: 'status-full' },
  { id: 4, day: '01', month: '4月', name: '月度冠军赛', desc: '月度积分排行奖励赛', status: '报名中', statusClass: 'status-open' },
]
</script>

<style scoped>
.club-detail-page {
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

.header-back, .header-right {
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

.club-header {
  background: var(--gradient-header);
  padding: 20px var(--spacing-lg) 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.club-logo {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.club-name {
  font-size: 20px;
  font-weight: 700;
  color: white;
  margin-bottom: 4px;
}

.club-id {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 10px;
}

.club-badges {
  display: flex;
  gap: 8px;
}

.badge {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: var(--radius-full);
}

.badge-verified {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.badge-level {
  background: rgba(255, 215, 0, 0.3);
  color: #FFD700;
}

.tab-row {
  display: flex;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-lighter);
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 12px 0;
  font-size: 14px;
  color: var(--text-secondary);
  position: relative;
}

.tab-item.active {
  color: var(--color-primary);
  font-weight: 600;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 2px;
  background: var(--color-primary);
  border-radius: 1px;
}

.stats-card {
  display: flex;
  align-items: center;
  justify-content: space-around;
  background: var(--bg-card);
  margin: 12px var(--spacing-lg);
  border-radius: var(--radius-md);
  padding: 16px;
  box-shadow: var(--shadow-card);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 11px;
  color: var(--text-tertiary);
}

.stat-divider {
  width: 1px;
  height: 28px;
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
  margin-bottom: 10px;
}

.intro-text {
  font-size: 13px;
  line-height: 1.8;
  color: var(--text-secondary);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.activity-date {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  background: #fff0f0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.date-day {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-primary);
  line-height: 1;
}

.date-month {
  font-size: 10px;
  color: var(--text-tertiary);
}

.activity-info {
  flex: 1;
}

.activity-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 2px;
}

.activity-desc {
  font-size: 11px;
  color: var(--text-tertiary);
}

.activity-status {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

.status-open {
  background: #fff0f0;
  color: var(--color-primary);
}

.status-soon {
  background: #E3F2FD;
  color: #1565C0;
}

.status-full {
  background: #f5f5f5;
  color: var(--text-tertiary);
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

.chat-btn {
  flex: 1;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 500;
  background: white;
}

.join-btn {
  flex: 1.5;
  height: 44px;
  background: var(--gradient-button);
  color: white;
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 600;
}
</style>
