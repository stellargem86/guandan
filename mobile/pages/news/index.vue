<template>
  <view class="page">
    <!-- 分类标签 -->
    <view class="category-tabs">
      <view
        class="cat-tab"
        :class="{ active: activeCategory === cat.value }"
        v-for="cat in categories"
        :key="cat.value"
        @tap="activeCategory = cat.value"
      >
        <text class="cat-tab-text" :class="{ active: activeCategory === cat.value }">{{ cat.label }}</text>
      </view>
    </view>

    <!-- 资讯列表 -->
    <scroll-view scroll-y class="news-list">
      <!-- 置顶大图文章 -->
      <view class="featured-article" @tap="goDetail(articles[0].id)" v-if="articles.length > 0">
        <view class="featured-cover">
          <text class="featured-emoji">{{ articles[0].emoji }}</text>
          <view class="featured-badge">
            <text class="badge-text">置顶</text>
          </view>
        </view>
        <view class="featured-info">
          <text class="featured-title">{{ articles[0].title }}</text>
          <view class="featured-meta">
            <text class="meta-author">{{ articles[0].author }}</text>
            <text class="meta-date">{{ articles[0].date }}</text>
            <text class="meta-views">{{ articles[0].views }}阅读</text>
          </view>
        </view>
      </view>

      <!-- 普通文章列表 -->
      <view class="article-item" v-for="article in restArticles" :key="article.id" @tap="goDetail(article.id)">
        <view class="article-content">
          <text class="article-title">{{ article.title }}</text>
          <view class="article-meta">
            <text class="meta-author">{{ article.author }}</text>
            <text class="meta-date">{{ article.date }}</text>
            <text class="meta-views">{{ article.views }}阅读</text>
          </view>
        </view>
        <view class="article-thumb">
          <text class="thumb-emoji">{{ article.emoji }}</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const activeCategory = ref('all')

const categories = [
  { label: '全部', value: 'all' },
  { label: '官方新闻', value: 'official' },
  { label: '新手入门', value: 'beginner' },
  { label: '掼蛋文化', value: 'culture' },
]

const allArticles = ref([
  {
    id: '1',
    title: '深掼会2024年度城市精英赛正式启动，百万奖金等你来战',
    emoji: '🏆',
    author: '深掼会官方',
    date: '2024-03-01',
    views: 12680,
    category: 'official',
  },
  {
    id: '2',
    title: '掼蛋新手必看：从零到入门的10个核心技巧',
    emoji: '📖',
    author: '王牌教练',
    date: '2024-02-28',
    views: 8956,
    category: 'beginner',
  },
  {
    id: '3',
    title: '掼蛋为何成为社交新宠？解读商务圈的「牌桌文化」',
    emoji: '🤝',
    author: '财经观察',
    date: '2024-02-25',
    views: 6782,
    category: 'culture',
  },
  {
    id: '4',
    title: '深掼会ELO段位系统全面升级，新增S+赛季段位',
    emoji: '⭐',
    author: '深掼会官方',
    date: '2024-02-22',
    views: 5430,
    category: 'official',
  },
  {
    id: '5',
    title: '高手进阶：掼蛋中的博弈论与概率思维',
    emoji: '🧠',
    author: '张大师',
    date: '2024-02-20',
    views: 4210,
    category: 'beginner',
  },
  {
    id: '6',
    title: '从安徽走向全国：掼蛋运动的发展历程',
    emoji: '📜',
    author: '文化研究院',
    date: '2024-02-18',
    views: 3890,
    category: 'culture',
  },
  {
    id: '7',
    title: '2024掼蛋规则最新修订说明',
    emoji: '📋',
    author: '深掼会官方',
    date: '2024-02-15',
    views: 7650,
    category: 'official',
  },
])

const articles = computed(() => {
  if (activeCategory.value === 'all') return allArticles.value
  return allArticles.value.filter((a) => a.category === activeCategory.value)
})

const restArticles = computed(() => articles.value.slice(1))

function goDetail(id: string) {
  uni.navigateTo({ url: `/pages/news/detail?id=${id}` })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 120rpx;
}

.category-tabs {
  display: flex;
  padding: 24rpx 32rpx;
  gap: 16rpx;
  overflow-x: auto;
}

.cat-tab {
  padding: 14rpx 28rpx;
  border-radius: 32rpx;
  background-color: #2a2a3e;
  white-space: nowrap;
  flex-shrink: 0;
}

.cat-tab.active {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
}

.cat-tab-text {
  font-size: 26rpx;
  color: #b0b0c0;
}

.cat-tab-text.active {
  color: #1a1a2e;
  font-weight: 600;
}

.news-list {
  padding: 0 32rpx;
  height: calc(100vh - 120rpx);
}

/* 置顶文章 */
.featured-article {
  background-color: #2a2a3e;
  border-radius: 24rpx;
  overflow: hidden;
  margin-bottom: 24rpx;
}

.featured-cover {
  height: 280rpx;
  background: linear-gradient(135deg, #32324a 0%, #1e1e32 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.featured-emoji {
  font-size: 96rpx;
}

.featured-badge {
  position: absolute;
  top: 16rpx;
  left: 16rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 8rpx;
  padding: 4rpx 16rpx;
}

.badge-text {
  font-size: 20rpx;
  color: #1a1a2e;
  font-weight: 600;
}

.featured-info {
  padding: 24rpx;
}

.featured-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: 12rpx;
  line-height: 1.4;
}

.featured-meta {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.meta-author {
  font-size: 22rpx;
  color: #f6c342;
}

.meta-date {
  font-size: 22rpx;
  color: #6b6b80;
}

.meta-views {
  font-size: 22rpx;
  color: #6b6b80;
}

/* 普通文章 */
.article-item {
  display: flex;
  align-items: center;
  padding: 24rpx;
  background-color: #2a2a3e;
  border-radius: 20rpx;
  margin-bottom: 16rpx;
}

.article-content {
  flex: 1;
  margin-right: 20rpx;
}

.article-title {
  font-size: 28rpx;
  font-weight: 500;
  color: #f5f5f5;
  margin-bottom: 12rpx;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.article-thumb {
  width: 140rpx;
  height: 100rpx;
  background: linear-gradient(135deg, #32324a 0%, #1e1e32 100%);
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.thumb-emoji {
  font-size: 40rpx;
}
</style>
