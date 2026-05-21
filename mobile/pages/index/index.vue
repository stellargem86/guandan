<template>
  <view class="page">
    <!-- 顶部搜索栏 -->
    <view class="header-bar">
      <view class="search-bar">
        <text class="search-icon">🔍</text>
        <input class="search-input" placeholder="搜索掼友、牌局、商户" placeholder-class="placeholder" />
      </view>
      <view class="location-btn">
        <text class="location-icon">📍</text>
        <text class="location-text">南京市</text>
      </view>
    </view>

    <!-- 分类标签 -->
    <view class="category-tabs">
      <view
        class="cat-tab"
        :class="{ active: activeTab === tab.value }"
        v-for="tab in tabs"
        :key="tab.value"
        @tap="activeTab = tab.value"
      >
        <text class="cat-tab-text" :class="{ active: activeTab === tab.value }">{{ tab.label }}</text>
      </view>
    </view>

    <scroll-view scroll-y class="content-scroll" @scrolltolower="loadMore">
      <!-- 热门约局 Section -->
      <view class="section" v-if="activeTab === 'all' || activeTab === 'match'">
        <view class="section-header">
          <text class="section-title">热门约局</text>
          <text class="section-more" @tap="goMatchmaking">更多 ></text>
        </view>
        <view class="match-list">
          <view class="match-card" v-for="match in hotMatches" :key="match.id" @tap="goMatchDetail(match.id)">
            <view class="match-info">
              <text class="match-title">{{ match.title }}</text>
              <view class="match-meta">
                <text class="match-time">🕐 {{ match.time }}</text>
                <text class="match-location">📍 {{ match.location }}</text>
              </view>
            </view>
            <view class="match-join-btn" @tap.stop="handleJoinMatch(match)">
              <text class="join-btn-text">加入</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 帖子动态列表 -->
      <view class="section">
        <view class="section-header">
          <view class="feed-tabs">
            <text class="feed-tab" :class="{ active: feedTab === 'latest' }" @tap="feedTab = 'latest'">最新动态</text>
            <text class="feed-tab" :class="{ active: feedTab === 'friends' }" @tap="feedTab = 'friends'">好友动态</text>
            <text class="feed-tab" :class="{ active: feedTab === 'recommend' }" @tap="feedTab = 'recommend'">商家推荐</text>
          </view>
        </view>

        <view class="post-list">
          <view class="post-card" v-for="post in posts" :key="post.id" @tap="goPostDetail(post.id)">
            <view class="post-header">
              <image v-if="post.avatar" :src="post.avatar" class="post-avatar" mode="aspectFill" />
              <view v-else class="post-avatar post-avatar-placeholder">
                <text class="avatar-char">{{ post.nickname.charAt(0) }}</text>
              </view>
              <view class="post-user">
                <view class="post-name-row">
                  <text class="post-nickname">{{ post.nickname }}</text>
                  <view class="post-badge" v-if="post.badge">
                    <text class="badge-text">{{ post.badge }}</text>
                  </view>
                </view>
                <text class="post-time">{{ post.time }}</text>
              </view>
            </view>
            <text class="post-content">{{ post.content }}</text>
            <view class="post-images" v-if="post.images && post.images.length > 0">
              <image
                v-for="(img, idx) in post.images"
                :key="idx"
                :src="img"
                class="post-img"
                mode="aspectFill"
              />
            </view>
            <view class="post-footer">
              <view class="post-action">
                <text class="action-icon">👍</text>
                <text class="action-num">{{ post.likes }}</text>
              </view>
              <view class="post-action">
                <text class="action-icon">💬</text>
                <text class="action-num">{{ post.comments }}</text>
              </view>
              <view class="post-action">
                <text class="action-icon">↗️</text>
                <text class="action-num">{{ post.shares }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- 发帖浮动按钮 -->
    <view class="fab-btn" @tap="goCreatePost">
      <text class="fab-icon">✏️</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('all')
const feedTab = ref('latest')

const tabs = [
  { label: '全部', value: 'all' },
  { label: '官方×掼蛋', value: 'official' },
  { label: '找人组局', value: 'match' },
  { label: '赛事一手', value: 'event' },
]

const hotMatches = ref([
  {
    id: '1',
    title: '南京3国际，3缺1',
    time: '05-21 14:00',
    location: '龙虎山茶馆',
  },
  {
    id: '2',
    title: '商务局，就差你了',
    time: '05-21 19:30',
    location: '五联发掼蛋室',
  },
  {
    id: '3',
    title: '掼蛋小王子约掼友',
    time: '05-22 10:00',
    location: '商家自荐享受',
  },
])

const posts = ref([
  {
    id: '1',
    avatar: '',
    nickname: '掼蛋小王子',
    badge: 'A+',
    time: '10分钟前',
    content: '周末有八个牌友一一结伴组三，全成掼蛋联盟的精英，谁来？',
    images: [],
    likes: 28,
    comments: 12,
    shares: 3,
  },
  {
    id: '2',
    avatar: '',
    nickname: '张大师',
    badge: '',
    time: '30分钟前',
    content: '昨天深掼会月赛夺冠了！连续三局对A打满贯，ELO涨了45分到2780，感谢队友老王的完美配合🎉',
    images: ['/static/demo/post1.jpg', '/static/demo/post2.jpg'],
    likes: 156,
    comments: 43,
    shares: 12,
  },
  {
    id: '3',
    avatar: '',
    nickname: '王姐·教育',
    badge: '',
    time: '2小时前',
    content: '分享一个实战技巧：当手持双王+同花顺时，不要急于出牌，先观察对手出牌节奏。昨晚靠这个策略逆转两局！',
    images: [],
    likes: 89,
    comments: 34,
    shares: 21,
  },
])

function goMatchmaking() {
  uni.navigateTo({ url: '/pages/index/matchmaking' })
}

function goMatchDetail(id: string) {
  uni.navigateTo({ url: `/pages/index/matchmaking?id=${id}` })
}

function handleJoinMatch(match: any) {
  uni.showToast({ title: `已加入「${match.title}」`, icon: 'none' })
}

function goPostDetail(id: string) {
  uni.navigateTo({ url: `/pages/index/post-detail?id=${id}` })
}

function goCreatePost() {
  uni.navigateTo({ url: '/pages/index/create-post' })
}

function loadMore() {
  // load more posts
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding-bottom: 120rpx;
}

/* 顶部搜索 */
.header-bar {
  display: flex;
  align-items: center;
  padding: 16rpx 24rpx;
  background-color: #FFFFFF;
  gap: 16rpx;
}

.search-bar {
  flex: 1;
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

.location-btn {
  display: flex;
  align-items: center;
  gap: 4rpx;
}

.location-icon {
  font-size: 28rpx;
}

.location-text {
  font-size: 24rpx;
  color: #333333;
}

/* 分类标签 */
.category-tabs {
  display: flex;
  padding: 16rpx 24rpx;
  gap: 16rpx;
  background-color: #FFFFFF;
  overflow-x: auto;
  border-bottom: 1rpx solid #F0F0F0;
}

.cat-tab {
  padding: 10rpx 24rpx;
  border-radius: 24rpx;
  background-color: #F5F5F5;
  white-space: nowrap;
  flex-shrink: 0;
}

.cat-tab.active {
  background-color: #C41E3A;
}

.cat-tab-text {
  font-size: 26rpx;
  color: #666666;
}

.cat-tab-text.active {
  color: #FFFFFF;
  font-weight: 500;
}

/* 内容区 */
.content-scroll {
  height: calc(100vh - 240rpx);
}

.section {
  margin-top: 16rpx;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 24rpx 12rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #333333;
}

.section-more {
  font-size: 24rpx;
  color: #C41E3A;
}

/* 热门约局 */
.match-list {
  padding: 0 24rpx;
}

.match-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #FFFFFF;
  border-radius: 12rpx;
  padding: 20rpx 24rpx;
  margin-bottom: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.match-info {
  flex: 1;
}

.match-title {
  font-size: 28rpx;
  font-weight: 500;
  color: #333333;
  margin-bottom: 8rpx;
}

.match-meta {
  display: flex;
  gap: 16rpx;
}

.match-time,
.match-location {
  font-size: 22rpx;
  color: #999999;
}

.match-join-btn {
  background-color: #C41E3A;
  border-radius: 24rpx;
  padding: 10rpx 28rpx;
}

.join-btn-text {
  font-size: 24rpx;
  color: #FFFFFF;
  font-weight: 500;
}

/* Feed标签 */
.feed-tabs {
  display: flex;
  gap: 32rpx;
}

.feed-tab {
  font-size: 28rpx;
  color: #999999;
  padding-bottom: 8rpx;
}

.feed-tab.active {
  color: #C41E3A;
  font-weight: 600;
  border-bottom: 4rpx solid #C41E3A;
}

/* 帖子列表 */
.post-list {
  padding: 0 24rpx;
}

.post-card {
  background-color: #FFFFFF;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.post-avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  margin-right: 16rpx;
}

.post-avatar-placeholder {
  background-color: #C41E3A;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-char {
  font-size: 28rpx;
  color: #FFFFFF;
  font-weight: 600;
}

.post-user {
  flex: 1;
}

.post-name-row {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.post-nickname {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
}

.post-badge {
  background-color: #FFF0F0;
  border-radius: 6rpx;
  padding: 2rpx 10rpx;
}

.badge-text {
  font-size: 20rpx;
  color: #C41E3A;
  font-weight: 500;
}

.post-time {
  font-size: 22rpx;
  color: #999999;
  margin-top: 4rpx;
}

.post-content {
  font-size: 28rpx;
  color: #333333;
  line-height: 1.6;
  margin-bottom: 16rpx;
}

.post-images {
  display: flex;
  gap: 12rpx;
  margin-bottom: 16rpx;
  flex-wrap: wrap;
}

.post-img {
  width: 200rpx;
  height: 200rpx;
  border-radius: 8rpx;
  background-color: #F5F5F5;
}

.post-footer {
  display: flex;
  align-items: center;
  gap: 48rpx;
  padding-top: 16rpx;
  border-top: 1rpx solid #F0F0F0;
}

.post-action {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.action-icon {
  font-size: 28rpx;
}

.action-num {
  font-size: 24rpx;
  color: #999999;
}

/* 浮动按钮 */
.fab-btn {
  position: fixed;
  right: 32rpx;
  bottom: 180rpx;
  width: 96rpx;
  height: 96rpx;
  background-color: #C41E3A;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 24rpx rgba(196, 30, 58, 0.3);
}

.fab-icon {
  font-size: 36rpx;
}
</style>
