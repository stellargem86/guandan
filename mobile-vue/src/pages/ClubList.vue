<template>
  <div class="page clubs-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-title">俱乐部</div>
        <div class="header-action">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        </div>
      </div>
    </div>

    <!-- Search -->
    <div class="search-section">
      <div class="search-bar">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" placeholder="搜索俱乐部名称..." readonly />
      </div>
    </div>

    <!-- Club List -->
    <div class="club-list">
      <div v-for="club in clubs" :key="club.id" class="club-card" @click="$router.push(`/club/${club.id}`)">
        <div class="club-icon" :style="{ background: club.color }">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5"><path d="M12 2L4 7v6c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V7l-8-5z"/></svg>
        </div>
        <div class="club-info">
          <div class="club-name-row">
            <h3 class="club-name">{{ club.name }}</h3>
            <span v-if="club.verified" class="verified-badge">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="#1976D2"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg>
            </span>
          </div>
          <div class="club-stats">
            <span class="club-members">会员 {{ club.members }}/{{ club.maxMembers }}</span>
            <span class="club-level">Lv.{{ club.level }}</span>
          </div>
          <div class="club-tags">
            <span v-for="tag in club.tags" :key="tag" class="club-tag">{{ tag }}</span>
          </div>
        </div>
        <button class="join-btn" @click.stop>申请加入</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const clubs = [
  {
    id: 1,
    name: '金陵掼蛋俱乐部',
    members: 128,
    maxMembers: 200,
    level: 5,
    verified: true,
    tags: ['高端', '商务'],
    color: 'linear-gradient(135deg, #8B1A2B, #C62828)'
  },
  {
    id: 2,
    name: '南京掼蛋精英会',
    members: 86,
    maxMembers: 150,
    level: 4,
    verified: true,
    tags: ['竞技', '培训'],
    color: 'linear-gradient(135deg, #1565C0, #42A5F5)'
  },
  {
    id: 3,
    name: '鼓楼掼蛋社',
    members: 64,
    maxMembers: 100,
    level: 3,
    verified: false,
    tags: ['休闲', '社交'],
    color: 'linear-gradient(135deg, #2E7D32, #66BB6A)'
  },
  {
    id: 4,
    name: '秦淮棋牌联盟',
    members: 156,
    maxMembers: 200,
    level: 5,
    verified: true,
    tags: ['综合', '赛事'],
    color: 'linear-gradient(135deg, #E65100, #FF9800)'
  },
  {
    id: 5,
    name: '玄武掼蛋联盟',
    members: 42,
    maxMembers: 80,
    level: 2,
    verified: false,
    tags: ['新手友好'],
    color: 'linear-gradient(135deg, #6A1B9A, #AB47BC)'
  },
  {
    id: 6,
    name: '建邺精英掼蛋社',
    members: 98,
    maxMembers: 150,
    level: 4,
    verified: true,
    tags: ['高端', '会员制'],
    color: 'linear-gradient(135deg, #004D40, #26A69A)'
  },
]
</script>

<style scoped>
.clubs-page {
  background: var(--bg-page);
  min-height: 100vh;
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
  justify-content: center;
  position: relative;
}

.header-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-white);
}

.header-action {
  position: absolute;
  right: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-section {
  padding: 12px var(--spacing-lg);
  background: var(--bg-card);
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f5f5f5;
  border-radius: var(--radius-full);
  padding: 10px 16px;
}

.search-bar input {
  flex: 1;
  background: transparent;
  font-size: 13px;
  color: var(--text-primary);
}

.search-bar input::placeholder {
  color: var(--text-tertiary);
}

.club-list {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.club-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px;
  box-shadow: var(--shadow-card);
  display: flex;
  align-items: center;
  gap: 12px;
}

.club-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.club-info {
  flex: 1;
  min-width: 0;
}

.club-name-row {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 4px;
}

.club-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.club-stats {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.club-members {
  font-size: 11px;
  color: var(--text-tertiary);
}

.club-level {
  font-size: 10px;
  padding: 1px 6px;
  background: #FFF3E0;
  color: #E65100;
  border-radius: var(--radius-full);
  font-weight: 600;
}

.club-tags {
  display: flex;
  gap: 4px;
}

.club-tag {
  font-size: 10px;
  padding: 2px 6px;
  background: #f5f5f5;
  color: var(--text-secondary);
  border-radius: var(--radius-full);
}

.join-btn {
  flex-shrink: 0;
  padding: 6px 12px;
  background: transparent;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
}
</style>
