<template>
  <view class="page">
    <!-- Tab切换 -->
    <view class="ranking-tabs">
      <view
        class="rank-tab"
        :class="{ active: activeTab === tab.value }"
        v-for="tab in tabs"
        :key="tab.value"
        @tap="activeTab = tab.value"
      >
        <text class="rank-tab-text" :class="{ active: activeTab === tab.value }">{{ tab.label }}</text>
      </view>
    </view>

    <!-- Top 3 展示 -->
    <view class="podium-section">
      <!-- 第二名 -->
      <view class="podium-item second">
        <view class="podium-avatar">
          <text class="podium-avatar-text">{{ topThree[1].avatar }}</text>
        </view>
        <text class="podium-name">{{ topThree[1].name }}</text>
        <text class="podium-score">{{ topThree[1].score }}</text>
        <view class="podium-base second">
          <text class="podium-rank">2</text>
        </view>
      </view>
      <!-- 第一名 -->
      <view class="podium-item first">
        <view class="crown">
          <text class="crown-icon">👑</text>
        </view>
        <view class="podium-avatar gold-border">
          <text class="podium-avatar-text">{{ topThree[0].avatar }}</text>
        </view>
        <text class="podium-name">{{ topThree[0].name }}</text>
        <text class="podium-score gold">{{ topThree[0].score }}</text>
        <view class="podium-base first">
          <text class="podium-rank">1</text>
        </view>
      </view>
      <!-- 第三名 -->
      <view class="podium-item third">
        <view class="podium-avatar">
          <text class="podium-avatar-text">{{ topThree[2].avatar }}</text>
        </view>
        <text class="podium-name">{{ topThree[2].name }}</text>
        <text class="podium-score">{{ topThree[2].score }}</text>
        <view class="podium-base third">
          <text class="podium-rank">3</text>
        </view>
      </view>
    </view>

    <!-- 排名列表 -->
    <view class="ranking-list-section">
      <view class="ranking-list-header">
        <text class="header-rank">排名</text>
        <text class="header-name">选手</text>
        <text class="header-elo">ELO</text>
        <text class="header-rate">胜率</text>
      </view>

      <scroll-view scroll-y class="ranking-scroll">
        <view class="ranking-item" v-for="item in rankingList" :key="item.rank">
          <text class="item-rank">{{ item.rank }}</text>
          <view class="item-user">
            <view class="item-avatar">
              <text class="item-avatar-text">{{ item.avatar }}</text>
            </view>
            <text class="item-name">{{ item.name }}</text>
          </view>
          <text class="item-elo">{{ item.score }}</text>
          <text class="item-rate">{{ item.winRate }}%</text>
        </view>
      </scroll-view>
    </view>

    <!-- 我的排名 -->
    <view class="my-ranking">
      <view class="my-ranking-inner">
        <text class="my-rank">第 86 名</text>
        <view class="my-info">
          <view class="my-avatar">
            <text class="my-avatar-text">我</text>
          </view>
          <text class="my-name">我的排名</text>
        </view>
        <text class="my-elo">2680</text>
        <text class="my-rate">62%</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('personal')

const tabs = [
  { label: '个人榜', value: 'personal' },
  { label: '俱乐部榜', value: 'club' },
  { label: '地区榜', value: 'region' },
]

const topThree = ref([
  { avatar: '张', name: '张大师', score: 3250 },
  { avatar: '李', name: '李教授', score: 3180 },
  { avatar: '王', name: '王牌手', score: 3120 },
])

const rankingList = ref([
  { rank: 4, avatar: '陈', name: '陈总', score: 3050, winRate: 78 },
  { rank: 5, avatar: '刘', name: '刘掌门', score: 2980, winRate: 75 },
  { rank: 6, avatar: '赵', name: '赵高手', score: 2920, winRate: 73 },
  { rank: 7, avatar: '周', name: '周教练', score: 2880, winRate: 71 },
  { rank: 8, avatar: '吴', name: '吴老师', score: 2850, winRate: 70 },
  { rank: 9, avatar: '郑', name: '郑先生', score: 2810, winRate: 69 },
  { rank: 10, avatar: '孙', name: '孙大侠', score: 2780, winRate: 68 },
  { rank: 11, avatar: '马', name: '马经理', score: 2750, winRate: 67 },
  { rank: 12, avatar: '朱', name: '朱总监', score: 2720, winRate: 66 },
  { rank: 13, avatar: '胡', name: '胡局长', score: 2700, winRate: 65 },
  { rank: 14, avatar: '林', name: '林博士', score: 2680, winRate: 64 },
  { rank: 15, avatar: '何', name: '何队长', score: 2650, winRate: 63 },
])
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 140rpx;
}

.ranking-tabs {
  display: flex;
  justify-content: center;
  padding: 24rpx 32rpx;
  gap: 8rpx;
  background-color: #1a1a2e;
}

.rank-tab {
  padding: 14rpx 36rpx;
  border-radius: 32rpx;
  background-color: #2a2a3e;
}

.rank-tab.active {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
}

.rank-tab-text {
  font-size: 26rpx;
  color: #b0b0c0;
}

.rank-tab-text.active {
  color: #1a1a2e;
  font-weight: 600;
}

/* 领奖台 */
.podium-section {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 48rpx 32rpx 32rpx;
  gap: 24rpx;
}

.podium-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.podium-item.first {
  margin-bottom: 20rpx;
}

.crown {
  margin-bottom: 8rpx;
}

.crown-icon {
  font-size: 40rpx;
}

.podium-avatar {
  width: 96rpx;
  height: 96rpx;
  background: linear-gradient(135deg, #3a3a50 0%, #2a2a3e 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8rpx;
  border: 3rpx solid #3a3a50;
}

.podium-avatar.gold-border {
  border: 3rpx solid #f6c342;
  width: 112rpx;
  height: 112rpx;
}

.podium-avatar-text {
  font-size: 32rpx;
  color: #f5f5f5;
  font-weight: 600;
}

.podium-name {
  font-size: 24rpx;
  color: #f5f5f5;
  font-weight: 500;
  margin-bottom: 4rpx;
}

.podium-score {
  font-size: 22rpx;
  color: #b0b0c0;
  margin-bottom: 12rpx;
}

.podium-score.gold {
  color: #f6c342;
  font-weight: 600;
}

.podium-base {
  width: 80rpx;
  height: 60rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8rpx 8rpx 0 0;
}

.podium-base.first {
  background: linear-gradient(180deg, #f6c342 0%, #d4a537 100%);
  height: 80rpx;
}

.podium-base.second {
  background: linear-gradient(180deg, #c0c0c0 0%, #a0a0a0 100%);
  height: 60rpx;
}

.podium-base.third {
  background: linear-gradient(180deg, #cd7f32 0%, #a0622a 100%);
  height: 48rpx;
}

.podium-rank {
  font-size: 28rpx;
  color: #1a1a2e;
  font-weight: 800;
}

/* 排名列表 */
.ranking-list-section {
  padding: 0 32rpx;
}

.ranking-list-header {
  display: flex;
  align-items: center;
  padding: 16rpx 20rpx;
  margin-bottom: 8rpx;
}

.header-rank {
  width: 80rpx;
  font-size: 22rpx;
  color: #6b6b80;
}

.header-name {
  flex: 1;
  font-size: 22rpx;
  color: #6b6b80;
}

.header-elo {
  width: 100rpx;
  font-size: 22rpx;
  color: #6b6b80;
  text-align: center;
}

.header-rate {
  width: 80rpx;
  font-size: 22rpx;
  color: #6b6b80;
  text-align: right;
}

.ranking-scroll {
  height: 600rpx;
}

.ranking-item {
  display: flex;
  align-items: center;
  padding: 20rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  margin-bottom: 12rpx;
}

.item-rank {
  width: 80rpx;
  font-size: 28rpx;
  color: #6b6b80;
  font-weight: 600;
}

.item-user {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.item-avatar {
  width: 56rpx;
  height: 56rpx;
  background: linear-gradient(135deg, #3a3a50 0%, #32324a 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-avatar-text {
  font-size: 22rpx;
  color: #f5f5f5;
}

.item-name {
  font-size: 26rpx;
  color: #f5f5f5;
}

.item-elo {
  width: 100rpx;
  font-size: 28rpx;
  color: #f6c342;
  font-weight: 600;
  text-align: center;
}

.item-rate {
  width: 80rpx;
  font-size: 26rpx;
  color: #10b981;
  text-align: right;
}

/* 我的排名 */
.my-ranking {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16rpx 32rpx;
  padding-bottom: calc(16rpx + env(safe-area-inset-bottom));
  background-color: #1a1a2e;
  border-top: 1rpx solid #3a3a50;
}

.my-ranking-inner {
  display: flex;
  align-items: center;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  padding: 20rpx;
  border: 1rpx solid rgba(246, 195, 66, 0.2);
}

.my-rank {
  width: 100rpx;
  font-size: 24rpx;
  color: #f6c342;
  font-weight: 600;
}

.my-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.my-avatar {
  width: 48rpx;
  height: 48rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.my-avatar-text {
  font-size: 20rpx;
  color: #1a1a2e;
  font-weight: 700;
}

.my-name {
  font-size: 26rpx;
  color: #f5f5f5;
}

.my-elo {
  width: 80rpx;
  font-size: 28rpx;
  color: #f6c342;
  font-weight: 600;
  text-align: center;
}

.my-rate {
  width: 60rpx;
  font-size: 26rpx;
  color: #10b981;
  text-align: right;
}
</style>
