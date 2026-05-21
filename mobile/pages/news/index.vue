<template>
  <view class="page">
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar">
        <text class="search-icon">🔍</text>
        <input class="search-input" placeholder="搜索资讯" placeholder-class="placeholder" />
      </view>
    </view>

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
    <scroll-view scroll-y class="news-scroll">
      <!-- 置顶大图 -->
      <view class="featured-card" v-if="articles.length > 0" @tap="goDetail(articles[0].id)">
        <view class="featured-img">
          <text class="featured-emoji">🏆</text>
        </view>
        <view class="featured-info">
          <text class="featured-title">{{ articles[0].title }}</text>
          <view class="featured-meta">
            <text class="meta-time">{{ articles[0].date }}</text>
            <text class="meta-views">{{ articles[0].views }}阅读</text>
          </view>
        </view>
      </view>

      <!-- 普通文章列表 -->
      <view class="article-list">
        <view class="article-card" v-for="article in restArticles" :key="article.id" @tap="goDetail(article.id)">
          <view class="article-content">
            <text class="article-title">{{ article.title }}</text>
            <view class="article-meta">
              <text class="meta-source">{{ article.source }}</text>
              <text class="meta-time">{{ article.date }}</text>
            </view>
          </view>
          <view class="article-thumb">
            <text class="thumb-emoji">{{ article.emoji }}</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const activeCategory = ref('recommend')

const categories = [
  { label: '推荐', value: 'recommend' },
  { label: '新闻', value: 'news' },
  { label: '教学', value: 'tutorial' },
  { label: '文化', value: 'culture' },
  { label: '运动', value: 'sports' },
]

const allArticles = ref([
  {
    id: '1',
    title: '2024南京掼蛋公开赛圆满闭幕',
    emoji: '🏆',
    source: '掼蛋平台',
    date: '05-18',
    views: 12680,
    category: 'news',
  },
  {
    id: '2',
    title: '掼蛋从0到1: 新手入门教学',
    emoji: '📖',
    source: '掼蛋学院',
    date: '05-15',
    views: 8956,
    category: 'tutorial',
  },
  {
    id: '3',
    title: '掼蛋高手进阶技巧分享',
    emoji: '🧠',
    source: '掼蛋大师',
    date: '05-12',
    views: 6782,
    category: 'tutorial',
  },
  {
    id: '4',
    title: '掼蛋文化：起源与发展',
    emoji: '📜',
    source: '文化频道',
    date: '05-10',
    views: 5430,
    category: 'culture',
  },
  {
    id: '5',
    title: '商务社交新玩法：掼蛋圈',
    emoji: '🤝',
    source: '商业观察',
    date: '05-08',
    views: 4210,
    category: 'news',
  },
])

const articles = computed(() => {
  if (activeCategory.value === 'recommend') return allArticles.value
  return allArticles.value.filter(a => a.category === activeCategory.value)
})

const restArticles = computed(() => articles.value.slice(1))

function goDetail(id: string) {
  uni.navigateTo({ url: `/pages/news/detail?id=${id}` })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding-bottom: 120rpx;
}

/* 搜索 */
.search-section {
  padding: 16rpx 24rpx;
  background-color: #FFFFFF;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #F5F5F5;
  border-radius: 32rpx;
  padding: 14rpx 24rpx;
  gap: 12rpx;
}

.search-icon {
  font-size: 28rpx;
}

.search-input {
  flex: 1;
  font-size: 26rpx;
  color: #333333;
}

.placeholder {
  color: #999999;
}

/* 分类 */
.category-tabs {
  display: flex;
  padding: 16rpx 24rpx;
  gap: 24rpx;
  background-color: #FFFFFF;
  border-bottom: 1rpx solid #F0F0F0;
}

.cat-tab {
  padding: 8rpx 0;
}

.cat-tab.active {
  border-bottom: 4rpx solid #C41E3A;
}

.cat-tab-text {
  font-size: 28rpx;
  color: #999999;
}

.cat-tab-text.active {
  color: #C41E3A;
  font-weight: 600;
}

/* 新闻列表 */
.news-scroll {
  height: calc(100vh - 200rpx);
  padding: 16rpx 24rpx;
}

/* 置顶大图 */
.featured-card {
  background-color: #FFFFFF;
  border-radius: 16rpx;
  overflow: hidden;
  margin-bottom: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.featured-img {
  height: 280rpx;
  background: linear-gradient(135deg, #FFF0F0 0%, #FFE0E0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.featured-emoji {
  font-size: 80rpx;
}

.featured-info {
  padding: 20rpx 24rpx;
}

.featured-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 12rpx;
  line-height: 1.4;
}

.featured-meta {
  display: flex;
  gap: 16rpx;
}

.meta-time {
  font-size: 22rpx;
  color: #999999;
}

.meta-views {
  font-size: 22rpx;
  color: #999999;
}

.meta-source {
  font-size: 22rpx;
  color: #C41E3A;
}

/* 普通文章 */
.article-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.article-card {
  display: flex;
  align-items: center;
  background-color: #FFFFFF;
  border-radius: 12rpx;
  padding: 20rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.article-content {
  flex: 1;
  margin-right: 16rpx;
}

.article-title {
  font-size: 28rpx;
  font-weight: 500;
  color: #333333;
  margin-bottom: 12rpx;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  gap: 16rpx;
}

.article-thumb {
  width: 140rpx;
  height: 100rpx;
  background-color: #FFF0F0;
  border-radius: 8rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.thumb-emoji {
  font-size: 40rpx;
}
</style>
