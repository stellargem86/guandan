<template>
  <view class="page">
    <!-- 文章标题区 -->
    <view class="article-header">
      <text class="article-title">深掼会2024年度城市精英赛正式启动，百万奖金等你来战</text>
      <view class="author-row">
        <view class="author-avatar">
          <text class="avatar-text">深</text>
        </view>
        <view class="author-info">
          <text class="author-name">深掼会官方</text>
          <text class="publish-time">2024-03-01 10:30 · 12680阅读</text>
        </view>
        <view class="follow-btn">
          <text class="follow-text">关注</text>
        </view>
      </view>
    </view>

    <!-- 文章内容 -->
    <view class="article-body">
      <text class="body-paragraph">
        2024年深掼会城市精英赛系列赛事于今日正式启动。本次赛事覆盖全国15座城市，总奖金池突破百万元，是国内规模最大的掼蛋竞技赛事之一。
      </text>

      <view class="body-image">
        <text class="image-emoji">🏆🎴🃏</text>
        <text class="image-caption">赛事宣传图</text>
      </view>

      <text class="body-subtitle">赛事亮点</text>

      <text class="body-paragraph">
        本次城市精英赛采用全新的ELO段位匹配系统，确保选手实力对等。赛事分为城市预选赛、大区晋级赛和全国总决赛三个阶段。每个城市预选赛设64-256个参赛名额。
      </text>

      <text class="body-paragraph">
        值得一提的是，本次赛事首次引入「商务社交」理念，参赛选手均为各行业精英人士，在牌桌上切磋牌技的同时，也能拓展人脉资源。
      </text>

      <view class="body-image">
        <text class="image-emoji">📊📈🎯</text>
        <text class="image-caption">ELO段位系统示意</text>
      </view>

      <text class="body-subtitle">报名方式</text>

      <text class="body-paragraph">
        选手可通过深掼会APP直接报名，报名费200元/人。VIP会员享受8折优惠。报名截止日期为3月10日。
      </text>

      <text class="body-paragraph">
        赛事组委会提醒：请参赛选手提前熟悉2024版竞赛规则，准时到场签到。更多赛事详情请关注深掼会官方通知。
      </text>

      <view class="body-quote">
        <text class="quote-text">"让掼蛋成为连接精英人群的社交纽带"  ——深掼会创始人</text>
      </view>
    </view>

    <!-- 相关文章 -->
    <view class="related-section">
      <text class="related-title">相关阅读</text>
      <view class="related-list">
        <view class="related-item" v-for="item in relatedArticles" :key="item.id" @tap="goDetail(item.id)">
          <text class="related-item-title">{{ item.title }}</text>
          <text class="related-item-views">{{ item.views }}阅读</text>
        </view>
      </view>
    </view>

    <!-- 底部互动 -->
    <view class="article-footer">
      <view class="footer-actions">
        <view class="footer-action">
          <text class="footer-icon">👍</text>
          <text class="footer-count">286</text>
        </view>
        <view class="footer-action">
          <text class="footer-icon">💬</text>
          <text class="footer-count">43</text>
        </view>
        <view class="footer-action">
          <text class="footer-icon">⭐</text>
          <text class="footer-count">收藏</text>
        </view>
        <view class="footer-action">
          <text class="footer-icon">🔄</text>
          <text class="footer-count">分享</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const relatedArticles = ref([
  { id: '4', title: '深掼会ELO段位系统全面升级，新增S+赛季段位', views: '5430' },
  { id: '7', title: '2024掼蛋规则最新修订说明', views: '7650' },
  { id: '2', title: '掼蛋新手必看：从零到入门的10个核心技巧', views: '8956' },
])

function goDetail(id: string) {
  uni.redirectTo({ url: `/pages/news/detail?id=${id}` })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 120rpx;
}

.article-header {
  padding: 32rpx;
  border-bottom: 1rpx solid #3a3a50;
}

.article-title {
  font-size: 38rpx;
  font-weight: 700;
  color: #f5f5f5;
  line-height: 1.4;
  margin-bottom: 24rpx;
}

.author-row {
  display: flex;
  align-items: center;
}

.author-avatar {
  width: 64rpx;
  height: 64rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16rpx;
}

.avatar-text {
  font-size: 24rpx;
  color: #1a1a2e;
  font-weight: 700;
}

.author-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.author-name {
  font-size: 28rpx;
  color: #f5f5f5;
  font-weight: 500;
}

.publish-time {
  font-size: 22rpx;
  color: #6b6b80;
}

.follow-btn {
  border: 1rpx solid rgba(246, 195, 66, 0.5);
  border-radius: 24rpx;
  padding: 10rpx 24rpx;
}

.follow-text {
  font-size: 24rpx;
  color: #f6c342;
}

/* 文章内容 */
.article-body {
  padding: 32rpx;
}

.body-paragraph {
  font-size: 30rpx;
  color: #e0e0e8;
  line-height: 1.8;
  margin-bottom: 24rpx;
  display: block;
}

.body-subtitle {
  font-size: 34rpx;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: 16rpx;
  margin-top: 16rpx;
  display: block;
}

.body-image {
  width: 100%;
  height: 300rpx;
  background: linear-gradient(135deg, #2a2a3e 0%, #32324a 100%);
  border-radius: 16rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 24rpx;
  gap: 12rpx;
}

.image-emoji {
  font-size: 56rpx;
}

.image-caption {
  font-size: 22rpx;
  color: #6b6b80;
}

.body-quote {
  background-color: #2a2a3e;
  border-left: 4rpx solid #f6c342;
  border-radius: 0 12rpx 12rpx 0;
  padding: 24rpx;
  margin: 24rpx 0;
}

.quote-text {
  font-size: 28rpx;
  color: #b0b0c0;
  font-style: italic;
  line-height: 1.6;
}

/* 相关阅读 */
.related-section {
  padding: 32rpx;
  border-top: 1rpx solid #3a3a50;
}

.related-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: 20rpx;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.related-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx;
  background-color: #2a2a3e;
  border-radius: 12rpx;
}

.related-item-title {
  flex: 1;
  font-size: 26rpx;
  color: #e0e0e8;
  margin-right: 16rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.related-item-views {
  font-size: 22rpx;
  color: #6b6b80;
  flex-shrink: 0;
}

/* 底部互动 */
.article-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20rpx 32rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  background-color: #1a1a2e;
  border-top: 1rpx solid #3a3a50;
}

.footer-actions {
  display: flex;
  justify-content: space-around;
}

.footer-action {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.footer-icon {
  font-size: 32rpx;
}

.footer-count {
  font-size: 24rpx;
  color: #6b6b80;
}
</style>
