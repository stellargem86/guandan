<template>
  <div class="page news-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-title">资讯</div>
      </div>
    </div>

    <!-- Category Tabs -->
    <div class="category-tabs">
      <div
        v-for="cat in categories"
        :key="cat"
        class="category-tab"
        :class="{ active: activeCat === cat }"
        @click="activeCat = cat"
      >{{ cat }}</div>
    </div>

    <!-- Featured Article -->
    <div class="featured-article" @click="$router.push('/news/1')">
      <div class="featured-image" :style="{ background: 'linear-gradient(135deg, #8B1A2B, #C62828)' }">
        <div class="featured-overlay">
          <span class="featured-tag">推荐</span>
          <h2 class="featured-title">2024全国掼蛋联赛规则重大更新：双王新玩法详解</h2>
        </div>
      </div>
    </div>

    <!-- Article List -->
    <div class="article-list">
      <div v-for="article in articles" :key="article.id" class="article-card" @click="$router.push(`/news/${article.id}`)">
        <div class="article-info">
          <h3 class="article-title">{{ article.title }}</h3>
          <div class="article-meta">
            <span class="meta-source">{{ article.source }}</span>
            <span class="meta-dot">·</span>
            <span class="meta-date">{{ article.date }}</span>
            <span class="meta-dot">·</span>
            <span class="meta-views">{{ article.views }}阅读</span>
          </div>
        </div>
        <div class="article-thumb" :style="{ background: article.thumbColor }">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
        </div>
      </div>
    </div>

    <!-- Bottom spacer -->
    <div class="bottom-spacer"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeCat = ref('推荐')
const categories = ['推荐', '新闻', '教学', '文化', '赛事']

const articles = [
  {
    id: 2,
    title: '掼蛋从0到1：新手入门完全教学指南',
    source: '掼蛋学院',
    date: '2小时前',
    views: '3.2万',
    thumbColor: 'linear-gradient(135deg, #667eea, #764ba2)'
  },
  {
    id: 3,
    title: '南京掼蛋文化：一桌牌局里的人情世故',
    source: '文化周刊',
    date: '5小时前',
    views: '1.8万',
    thumbColor: 'linear-gradient(135deg, #f093fb, #f5576c)'
  },
  {
    id: 4,
    title: '高手进阶：如何正确使用炸弹的时机选择',
    source: '掼蛋大师',
    date: '昨天',
    views: '5.6万',
    thumbColor: 'linear-gradient(135deg, #4facfe, #00f2fe)'
  },
  {
    id: 5,
    title: '2024年江苏省掼蛋联赛赛程公布',
    source: '官方公告',
    date: '昨天',
    views: '8.9万',
    thumbColor: 'linear-gradient(135deg, #43e97b, #38f9d7)'
  },
  {
    id: 6,
    title: '掼蛋牌桌礼仪：这些规矩你需要知道',
    source: '礼仪课堂',
    date: '2天前',
    views: '2.1万',
    thumbColor: 'linear-gradient(135deg, #fa709a, #fee140)'
  },
  {
    id: 7,
    title: '配合之道：双人掼蛋的沟通技巧与默契培养',
    source: '掼蛋学院',
    date: '3天前',
    views: '4.3万',
    thumbColor: 'linear-gradient(135deg, #a18cd1, #fbc2eb)'
  },
]
</script>

<style scoped>
.news-page {
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
}

.header-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-white);
}

.category-tabs {
  display: flex;
  background: var(--bg-card);
  padding: 0 var(--spacing-lg);
  border-bottom: 1px solid var(--border-lighter);
}

.category-tab {
  padding: 12px 16px;
  font-size: 14px;
  color: var(--text-secondary);
  position: relative;
  white-space: nowrap;
}

.category-tab.active {
  color: var(--color-primary);
  font-weight: 600;
}

.category-tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: var(--color-primary);
  border-radius: 1px;
}

.featured-article {
  margin: 12px var(--spacing-lg);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-card);
}

.featured-image {
  height: 180px;
  position: relative;
  display: flex;
  align-items: flex-end;
}

.featured-overlay {
  width: 100%;
  padding: 16px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
}

.featured-tag {
  font-size: 10px;
  padding: 2px 8px;
  background: var(--color-primary);
  color: white;
  border-radius: var(--radius-full);
  margin-bottom: 6px;
  display: inline-block;
}

.featured-title {
  font-size: 16px;
  font-weight: 600;
  color: white;
  line-height: 1.4;
}

.article-list {
  padding: 0 var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: 1px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  margin: 0 var(--spacing-lg);
  overflow: hidden;
  box-shadow: var(--shadow-card);
}

.article-card {
  display: flex;
  gap: 12px;
  padding: 14px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-lighter);
}

.article-card:last-child {
  border-bottom: none;
}

.article-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.article-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: var(--text-tertiary);
  margin-top: 8px;
}

.meta-dot {
  color: var(--text-tertiary);
}

.article-thumb {
  width: 80px;
  height: 60px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.bottom-spacer {
  height: calc(var(--tabbar-height) + 20px);
}
</style>
