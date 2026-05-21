<template>
  <view class="page">
    <!-- 顶部标题区 -->
    <view class="header">
      <view class="header-title">
        <text class="title">掼友圈</text>
        <text class="subtitle">同城掼蛋 约局交友</text>
      </view>
      <view class="header-action" @tap="goCreatePost">
        <text class="action-icon">✏️</text>
      </view>
    </view>

    <!-- 快捷功能入口 -->
    <view class="quick-actions">
      <view class="action-item" @tap="goMap">
        <view class="action-icon-wrap">
          <text class="action-emoji">📍</text>
        </view>
        <text class="action-label">地图找局</text>
      </view>
      <view class="action-item" @tap="goMatchmaking">
        <view class="action-icon-wrap">
          <text class="action-emoji">🎯</text>
        </view>
        <text class="action-label">一键组局</text>
      </view>
      <view class="action-item" @tap="goNetwork">
        <view class="action-icon-wrap">
          <text class="action-emoji">🤝</text>
        </view>
        <text class="action-label">商务人脉</text>
      </view>
      <view class="action-item" @tap="goEvents">
        <view class="action-icon-wrap">
          <text class="action-emoji">🔥</text>
        </view>
        <text class="action-label">热门活动</text>
      </view>
    </view>

    <!-- 热门牌场 -->
    <view class="section-header">
      <text class="section-title">热门牌场</text>
      <text class="section-more" @tap="goMap">查看全部 ›</text>
    </view>

    <scroll-view scroll-x class="venue-scroll">
      <view class="venue-list">
        <view class="venue-card" v-for="venue in venues" :key="venue.id" @tap="goMerchantDetail(venue.id)">
          <view class="venue-cover">
            <text class="venue-cover-text">{{ venue.coverEmoji }}</text>
          </view>
          <text class="venue-name">{{ venue.name }}</text>
          <view class="venue-info">
            <text class="venue-rating">⭐ {{ venue.rating }}</text>
            <text class="venue-distance">{{ venue.distance }}</text>
          </view>
        </view>
      </view>
    </scroll-view>

    <!-- Feed帖子列表 -->
    <view class="section-header">
      <text class="section-title">掼友动态</text>
    </view>

    <view class="feed-list">
      <view class="post-card" v-for="post in posts" :key="post.id" @tap="goPostDetail(post.id)">
        <view class="post-header">
          <view class="post-avatar">
            <text class="avatar-text">{{ post.avatar }}</text>
          </view>
          <view class="post-user-info">
            <text class="post-nickname">{{ post.nickname }}</text>
            <text class="post-time">{{ post.time }}</text>
          </view>
          <view class="post-tag" v-if="post.tag">
            <text class="post-tag-text">{{ post.tag }}</text>
          </view>
        </view>
        <text class="post-content">{{ post.content }}</text>
        <view class="post-images" v-if="post.images && post.images.length">
          <view class="post-image" v-for="(img, idx) in post.images" :key="idx">
            <text class="img-placeholder">{{ img }}</text>
          </view>
        </view>
        <view class="post-footer">
          <view class="post-action">
            <text class="action-text">👍 {{ post.likes }}</text>
          </view>
          <view class="post-action">
            <text class="action-text">💬 {{ post.comments }}</text>
          </view>
          <view class="post-action">
            <text class="action-text">🔄 {{ post.shares }}</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const venues = ref([
  { id: '1', name: '金陵棋牌会所', rating: '4.9', distance: '1.2km', coverEmoji: '🏆' },
  { id: '2', name: '龙虎山茶馆', rating: '4.8', distance: '2.0km', coverEmoji: '🍵' },
  { id: '3', name: '紫金阁牌室', rating: '4.7', distance: '3.5km', coverEmoji: '🎴' },
  { id: '4', name: '秦淮雅集', rating: '4.9', distance: '4.1km', coverEmoji: '🏮' },
])

const posts = ref([
  {
    id: '1',
    avatar: '张',
    nickname: '张总·金融',
    time: '10分钟前',
    tag: '约局',
    content: '今晚8点金陵棋牌会所，三缺一，段位A以上优先，结束后聚餐！有意者私信我，地址：建邺区奥体大街68号',
    images: ['🃏', '🎴', '🀄'],
    likes: 28,
    comments: 12,
    shares: 3,
  },
  {
    id: '2',
    avatar: '李',
    nickname: '李总·科技',
    time: '30分钟前',
    tag: '战报',
    content: '昨天深掼会月赛夺冠了！连续三局对A打满贯，ELO涨了45分到2780，感谢队友老王的完美配合🎉 下个月继续冲！',
    images: ['🏆', '📊'],
    likes: 156,
    comments: 43,
    shares: 12,
  },
  {
    id: '3',
    avatar: '王',
    nickname: '王姐·教育',
    time: '2小时前',
    tag: '心得',
    content: '分享一个实战技巧：当手持双王+同花顺时，不要急于出牌，先观察对手出牌节奏。昨晚就是靠这个策略逆转了两局，段位从B+升到A-',
    images: [],
    likes: 89,
    comments: 34,
    shares: 21,
  },
  {
    id: '4',
    avatar: '陈',
    nickname: '陈总·地产',
    time: '3小时前',
    tag: '推荐',
    content: '强烈推荐紫金阁牌室！环境优雅，服务到位，茶水免费，还有专业的计分系统。老板是深掼会的会员，给咱们打8折💰',
    images: ['📷', '📷', '📷'],
    likes: 67,
    comments: 18,
    shares: 8,
  },
])

function goMap() {
  uni.navigateTo({ url: '/pages/index/map' })
}

function goMatchmaking() {
  uni.navigateTo({ url: '/pages/index/matchmaking' })
}

function goNetwork() {
  uni.showToast({ title: '商务人脉功能即将开放', icon: 'none' })
}

function goEvents() {
  uni.switchTab({ url: '/pages/events/index' })
}

function goCreatePost() {
  uni.navigateTo({ url: '/pages/index/create-post' })
}

function goMerchantDetail(id: string) {
  uni.navigateTo({ url: `/pages/index/merchant-detail?id=${id}` })
}

function goPostDetail(id: string) {
  uni.navigateTo({ url: `/pages/index/post-detail?id=${id}` })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 120rpx;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32rpx 32rpx 16rpx;
}

.header-title {
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 44rpx;
  font-weight: 700;
  color: #f5f5f5;
}

.subtitle {
  font-size: 24rpx;
  color: #6b6b80;
  margin-top: 4rpx;
}

.header-action {
  width: 72rpx;
  height: 72rpx;
  background-color: #2a2a3e;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-icon {
  font-size: 32rpx;
}

/* 快捷功能入口 */
.quick-actions {
  display: flex;
  justify-content: space-around;
  padding: 24rpx 32rpx 32rpx;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
}

.action-icon-wrap {
  width: 96rpx;
  height: 96rpx;
  background: linear-gradient(135deg, rgba(246, 195, 66, 0.15) 0%, rgba(212, 165, 55, 0.08) 100%);
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1rpx solid rgba(246, 195, 66, 0.2);
}

.action-emoji {
  font-size: 40rpx;
}

.action-label {
  font-size: 22rpx;
  color: #b0b0c0;
}

/* 区域标题 */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx 32rpx 16rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #f5f5f5;
}

.section-more {
  font-size: 24rpx;
  color: #f6c342;
}

/* 热门牌场横滑 */
.venue-scroll {
  white-space: nowrap;
  padding-left: 32rpx;
}

.venue-list {
  display: flex;
  gap: 20rpx;
  padding-right: 32rpx;
}

.venue-card {
  display: inline-flex;
  flex-direction: column;
  width: 240rpx;
  background-color: #2a2a3e;
  border-radius: 20rpx;
  overflow: hidden;
  flex-shrink: 0;
}

.venue-cover {
  width: 240rpx;
  height: 160rpx;
  background: linear-gradient(135deg, #32324a 0%, #2a2a3e 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.venue-cover-text {
  font-size: 56rpx;
}

.venue-name {
  font-size: 24rpx;
  font-weight: 500;
  color: #f5f5f5;
  padding: 12rpx 16rpx 4rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.venue-info {
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 4rpx 16rpx 16rpx;
}

.venue-rating {
  font-size: 20rpx;
  color: #f6c342;
}

.venue-distance {
  font-size: 20rpx;
  color: #6b6b80;
}

/* 帖子Feed */
.feed-list {
  padding: 0 32rpx;
}

.post-card {
  background-color: #2a2a3e;
  border-radius: 24rpx;
  padding: 28rpx;
  margin-bottom: 24rpx;
}

.post-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.post-avatar {
  width: 72rpx;
  height: 72rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16rpx;
}

.avatar-text {
  font-size: 28rpx;
  color: #1a1a2e;
  font-weight: 700;
}

.post-user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.post-nickname {
  font-size: 28rpx;
  font-weight: 600;
  color: #f5f5f5;
}

.post-time {
  font-size: 22rpx;
  color: #6b6b80;
  margin-top: 4rpx;
}

.post-tag {
  background-color: rgba(246, 195, 66, 0.12);
  border-radius: 8rpx;
  padding: 6rpx 16rpx;
}

.post-tag-text {
  font-size: 20rpx;
  color: #f6c342;
}

.post-content {
  font-size: 28rpx;
  color: #e0e0e8;
  line-height: 1.6;
  margin-bottom: 16rpx;
  white-space: normal;
  word-break: break-all;
}

.post-images {
  display: flex;
  gap: 12rpx;
  margin-bottom: 16rpx;
  flex-wrap: wrap;
}

.post-image {
  width: 180rpx;
  height: 180rpx;
  background-color: #1e1e32;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.img-placeholder {
  font-size: 48rpx;
}

.post-footer {
  display: flex;
  align-items: center;
  gap: 40rpx;
  padding-top: 16rpx;
  border-top: 1rpx solid #3a3a50;
}

.post-action {
  display: flex;
  align-items: center;
}

.action-text {
  font-size: 24rpx;
  color: #6b6b80;
}
</style>
