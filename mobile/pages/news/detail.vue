<template>
  <view class="page">
    <!-- 文章标题 -->
    <view class="article-header">
      <text class="article-title">掼蛋从0到1：新手入门教学</text>
      <view class="article-meta">
        <text class="meta-source">掼蛋学院</text>
        <text class="meta-dot">·</text>
        <text class="meta-time">2024-05-15</text>
      </view>
    </view>

    <!-- 文章正文 -->
    <view class="article-body">
      <text class="body-subtitle">一、掼蛋介绍</text>
      <text class="body-paragraph">
        掼蛋是一种四人牌类游戏，源于安徽，近年来在全国范围内广泛流行。它融合了策略、配合与运气，是商务社交和休闲娱乐的绝佳选择。
      </text>

      <view class="body-image">
        <text class="image-emoji">🃏🎴</text>
      </view>

      <text class="body-subtitle">二、基本规则</text>
      <text class="body-paragraph">
        如何开始掼蛋的对局？首先需要四名玩家，分为两组对家，使用两副牌。游戏的目标是通过配合尽快出完手中的牌，赢取升级机会。
      </text>

      <text class="body-paragraph">
        出牌顺序为逆时针方向，玩家需要根据上家出的牌型来跟牌。掌握基础牌型如单张、对子、三条、顺子、炸弹等是入门的第一步。
      </text>

      <text class="body-subtitle">三、进阶技巧</text>
      <text class="body-paragraph">
        当熟悉了基本规则后，需要学习如何配合队友。良好的信号传递和牌力判断是赢得比赛的关键。
      </text>
    </view>

    <!-- 底部互动栏 -->
    <view class="article-footer">
      <view class="footer-left">
        <view class="footer-action">
          <text class="footer-icon">👍</text>
          <text class="footer-count">123</text>
        </view>
        <view class="footer-action">
          <text class="footer-icon">💬</text>
          <text class="footer-count">45</text>
        </view>
      </view>
      <view class="footer-right">
        <view class="footer-action">
          <text class="footer-icon">⭐</text>
          <text class="footer-text">收藏</text>
        </view>
        <view class="footer-action">
          <text class="footer-icon">↗️</text>
          <text class="footer-text">分享</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #FFFFFF;
  padding-bottom: 120rpx;
}

/* 头部 */
.article-header {
  padding: 32rpx 24rpx 24rpx;
  border-bottom: 1rpx solid #F0F0F0;
}

.article-title {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
  line-height: 1.4;
  margin-bottom: 16rpx;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.meta-source {
  font-size: 24rpx;
  color: #C41E3A;
}

.meta-dot {
  font-size: 24rpx;
  color: #CCCCCC;
}

.meta-time {
  font-size: 24rpx;
  color: #999999;
}

/* 正文 */
.article-body {
  padding: 24rpx;
}

.body-subtitle {
  font-size: 32rpx;
  font-weight: 600;
  color: #333333;
  margin-top: 32rpx;
  margin-bottom: 16rpx;
  display: block;
}

.body-paragraph {
  font-size: 28rpx;
  color: #555555;
  line-height: 2;
  margin-bottom: 20rpx;
  display: block;
}

.body-image {
  width: 100%;
  height: 300rpx;
  background-color: #FFF5F5;
  border-radius: 12rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 24rpx 0;
}

.image-emoji {
  font-size: 64rpx;
}

/* 底部互动 */
.article-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 24rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  background-color: #FFFFFF;
  border-top: 1rpx solid #F0F0F0;
}

.footer-left,
.footer-right {
  display: flex;
  gap: 32rpx;
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
  color: #666666;
}

.footer-text {
  font-size: 24rpx;
  color: #666666;
}
</style>
