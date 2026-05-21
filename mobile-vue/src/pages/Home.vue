<template>
  <div class="page home-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-title">掼友圈</div>
        <div class="header-location">
          <span class="location-dot"></span>
          <span>南京市</span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </div>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="search-wrapper">
      <div class="search-bar">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="text" placeholder="搜索牌友、牌场、赛事..." readonly />
      </div>
    </div>

    <!-- Tab Pills -->
    <div class="tab-pills">
      <div
        v-for="tab in tabs"
        :key="tab"
        class="tab-pill"
        :class="{ active: activeTab === tab }"
        @click="activeTab = tab"
      >{{ tab }}</div>
    </div>

    <!-- Hot Venues Section -->
    <div class="section">
      <div class="section-header">
        <span class="section-title">热门牌场</span>
        <span class="section-more">查看全部 ›</span>
      </div>
      <div class="venue-scroll">
        <div v-for="venue in venues" :key="venue.name" class="venue-chip" @click="$router.push('/map')">
          <div class="venue-info">
            <span class="venue-name">{{ venue.name }}</span>
            <span class="venue-count">{{ venue.count }}人在玩</span>
          </div>
          <span class="venue-join">加入</span>
        </div>
      </div>
    </div>

    <!-- Feed Section -->
    <div class="section">
      <div class="section-header">
        <span class="section-title">最新动态</span>
      </div>
      <div class="feed-list">
        <div v-for="post in posts" :key="post.id" class="feed-card">
          <div class="feed-header">
            <div class="feed-avatar" :style="{ background: post.avatarColor }">
              {{ post.author[0] }}
            </div>
            <div class="feed-meta">
              <span class="feed-author">{{ post.author }}</span>
              <span class="feed-time">{{ post.time }}</span>
            </div>
          </div>
          <div class="feed-body">
            <div class="feed-text">{{ post.content }}</div>
            <div v-if="post.image" class="feed-image">
              <div class="image-placeholder" :style="{ background: post.imageColor }">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
              </div>
            </div>
          </div>
          <div class="feed-actions">
            <div class="feed-action">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              <span>{{ post.comments }}</span>
            </div>
            <div class="feed-action">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              <span>{{ post.likes }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Button -->
    <div class="cta-wrapper">
      <button class="cta-button" @click="$router.push('/map')">立即进入</button>
    </div>

    <!-- Bottom spacing for tab bar -->
    <div class="bottom-spacer"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('全部')
const tabs = ['全部', '掼蛋x精醒', '好友动态', '赛事资讯', '牌友推荐']

const venues = [
  { name: '南京1群场·商务局', count: 24 },
  { name: '商务局VIP室', count: 16 },
  { name: '金陵掼蛋俱乐部', count: 32 },
  { name: '玄武湖畔茶室', count: 8 },
  { name: '新街口棋牌室', count: 12 },
]

const posts = [
  {
    id: 1,
    author: '张三丰',
    avatarColor: 'linear-gradient(135deg, #667eea, #764ba2)',
    time: '2分钟前',
    content: '今天在同庆楼打了三局掼蛋，连赢三把！最后一局对手差点炸了我的连对，还好稳住了。周末有没有人组局？',
    comments: 12,
    likes: 36,
    image: true,
    imageColor: 'linear-gradient(135deg, #f093fb, #f5576c)'
  },
  {
    id: 2,
    author: '李掼王',
    avatarColor: 'linear-gradient(135deg, #4facfe, #00f2fe)',
    time: '15分钟前',
    content: '掼蛋新手入门分享：记住一个原则，有炸弹不轻易出，等对手快走完再一波带走。今天用这招成功翻盘两次！',
    comments: 28,
    likes: 89,
    image: false,
    imageColor: ''
  },
  {
    id: 3,
    author: '王大炸',
    avatarColor: 'linear-gradient(135deg, #43e97b, #38f9d7)',
    time: '1小时前',
    content: '南京市掼蛋锦标赛报名开始啦！奖金池10万，128个名额先到先得。上次比赛氛围超好，这次一定要拿前三！',
    comments: 45,
    likes: 156,
    image: true,
    imageColor: 'linear-gradient(135deg, #fa709a, #fee140)'
  },
  {
    id: 4,
    author: '赵铁柱',
    avatarColor: 'linear-gradient(135deg, #a18cd1, #fbc2eb)',
    time: '2小时前',
    content: '刚加入了金陵掼蛋俱乐部，里面高手如云！昨天学到一个新战术：双王配合连炸，对面直接愣住了。',
    comments: 8,
    likes: 42,
    image: false,
    imageColor: ''
  },
]
</script>

<style scoped>
.home-page {
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
  justify-content: space-between;
}

.header-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-white);
  letter-spacing: 1px;
}

.header-location {
  display: flex;
  align-items: center;
  gap: 4px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 12px;
}

.location-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #4CAF50;
}

.search-wrapper {
  background: var(--gradient-header);
  padding: 0 var(--spacing-lg) 12px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: var(--radius-full);
  padding: 8px 16px;
}

.search-bar input {
  flex: 1;
  background: transparent;
  font-size: 13px;
  color: var(--text-secondary);
}

.search-bar input::placeholder {
  color: var(--text-tertiary);
}

.tab-pills {
  display: flex;
  gap: 8px;
  padding: 12px var(--spacing-lg);
  overflow-x: auto;
  background: var(--bg-card);
}

.tab-pill {
  flex-shrink: 0;
  padding: 6px 14px;
  border-radius: var(--radius-full);
  font-size: 13px;
  color: var(--text-secondary);
  background: #f5f5f5;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.tab-pill.active {
  background: var(--color-primary);
  color: var(--text-white);
}

.section {
  padding: var(--spacing-lg);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.section-more {
  font-size: 12px;
  color: var(--text-tertiary);
}

.venue-scroll {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.venue-chip {
  flex-shrink: 0;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  box-shadow: var(--shadow-card);
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 160px;
}

.venue-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.venue-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
}

.venue-count {
  font-size: 11px;
  color: var(--text-tertiary);
}

.venue-join {
  font-size: 11px;
  color: var(--text-white);
  background: var(--color-primary);
  padding: 3px 8px;
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.feed-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.feed-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-card);
}

.feed-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.feed-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.feed-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.feed-author {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.feed-time {
  font-size: 11px;
  color: var(--text-tertiary);
}

.feed-body {
  display: flex;
  gap: 12px;
}

.feed-text {
  flex: 1;
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-primary);
}

.feed-image {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feed-actions {
  display: flex;
  gap: 20px;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--border-lighter);
}

.feed-action {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.cta-wrapper {
  padding: 0 var(--spacing-lg) var(--spacing-lg);
}

.cta-button {
  width: 100%;
  height: 48px;
  background: var(--gradient-button);
  color: var(--text-white);
  border-radius: var(--radius-full);
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1px;
  box-shadow: 0 4px 16px rgba(155, 27, 48, 0.3);
}

.bottom-spacer {
  height: calc(var(--tabbar-height) + 20px);
}
</style>
