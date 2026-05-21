<template>
  <view class="page">
    <!-- 封面 -->
    <view class="cover-section">
      <view class="cover-bg">
        <text class="cover-emoji">🏆</text>
      </view>
      <view class="cover-status">
        <text class="status-badge">报名中</text>
      </view>
    </view>

    <!-- 基本信息 -->
    <view class="info-section">
      <text class="event-title">深掼会·2024南京城市精英赛</text>
      <view class="organizer-row">
        <view class="organizer-avatar">
          <text class="avatar-text">深</text>
        </view>
        <text class="organizer-name">深掼会官方</text>
        <view class="official-badge">
          <text class="official-text">官方</text>
        </view>
      </view>

      <view class="info-items">
        <view class="info-row">
          <text class="info-icon">📅</text>
          <view class="info-content">
            <text class="info-label">比赛时间</text>
            <text class="info-value">2024年3月15日 09:00 - 18:00</text>
          </view>
        </view>
        <view class="info-row">
          <text class="info-icon">📍</text>
          <view class="info-content">
            <text class="info-label">比赛地点</text>
            <text class="info-value">南京奥体中心·多功能厅</text>
          </view>
        </view>
        <view class="info-row">
          <text class="info-icon">👥</text>
          <view class="info-content">
            <text class="info-label">报名情况</text>
            <text class="info-value">已报名 198/256 人</text>
          </view>
        </view>
        <view class="info-row">
          <text class="info-icon">💰</text>
          <view class="info-content">
            <text class="info-label">报名费用</text>
            <text class="info-value gold">¥200/人</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 奖金设置 -->
    <view class="section">
      <text class="section-title">🏅 奖金设置</text>
      <view class="prize-list">
        <view class="prize-item">
          <text class="prize-rank gold">冠军</text>
          <text class="prize-amount">¥10,000 + 金牌</text>
        </view>
        <view class="prize-item">
          <text class="prize-rank silver">亚军</text>
          <text class="prize-amount">¥5,000 + 银牌</text>
        </view>
        <view class="prize-item">
          <text class="prize-rank bronze">季军</text>
          <text class="prize-amount">¥3,000 + 铜牌</text>
        </view>
        <view class="prize-item">
          <text class="prize-rank">4-8名</text>
          <text class="prize-amount">¥1,000</text>
        </view>
      </view>
    </view>

    <!-- 赛制规则 -->
    <view class="section">
      <text class="section-title">📋 赛制规则</text>
      <view class="rules-content">
        <text class="rule-text">1. 采用国家体育总局掼蛋竞赛规则</text>
        <text class="rule-text">2. 小组赛阶段：随机分组，每组4对，循环赛制</text>
        <text class="rule-text">3. 淘汰赛阶段：小组前2名晋级，单败淘汰</text>
        <text class="rule-text">4. 决赛阶段：三局两胜制</text>
        <text class="rule-text">5. 比赛使用电子计分系统，全程录像</text>
      </view>
    </view>

    <!-- 时间安排 -->
    <view class="section">
      <text class="section-title">⏰ 时间安排</text>
      <view class="schedule-list">
        <view class="schedule-item">
          <text class="schedule-time">08:30</text>
          <text class="schedule-event">签到入场</text>
        </view>
        <view class="schedule-item">
          <text class="schedule-time">09:00</text>
          <text class="schedule-event">开幕式</text>
        </view>
        <view class="schedule-item">
          <text class="schedule-time">09:30</text>
          <text class="schedule-event">小组赛第一轮</text>
        </view>
        <view class="schedule-item">
          <text class="schedule-time">12:00</text>
          <text class="schedule-event">午餐休息</text>
        </view>
        <view class="schedule-item">
          <text class="schedule-time">13:30</text>
          <text class="schedule-event">淘汰赛</text>
        </view>
        <view class="schedule-item">
          <text class="schedule-time">16:00</text>
          <text class="schedule-event">决赛</text>
        </view>
        <view class="schedule-item">
          <text class="schedule-time">17:30</text>
          <text class="schedule-event">颁奖典礼</text>
        </view>
      </view>
    </view>

    <!-- 已报名选手预览 -->
    <view class="section">
      <text class="section-title">👥 已报名 (198人)</text>
      <view class="enrolled-preview">
        <view class="enrolled-avatar" v-for="(p, idx) in enrolledPreview" :key="idx">
          <text class="enrolled-text">{{ p }}</text>
        </view>
        <view class="enrolled-more">
          <text class="more-text">+190</text>
        </view>
      </view>
    </view>

    <!-- 底部报名按钮 -->
    <view class="bottom-bar">
      <view class="price-info">
        <text class="price-label">报名费</text>
        <text class="price-value">¥200</text>
      </view>
      <view class="enroll-btn" @tap="handleEnroll">
        <text class="enroll-text">立即报名</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const enrolledPreview = ref(['张', '李', '王', '陈', '刘', '赵', '周', '吴'])

function handleEnroll() {
  uni.showToast({ title: '报名成功！', icon: 'success' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 160rpx;
}

.cover-section {
  position: relative;
  height: 320rpx;
}

.cover-bg {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #2a2a3e 0%, #32324a 50%, #1e1e32 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-emoji {
  font-size: 120rpx;
}

.cover-status {
  position: absolute;
  top: 24rpx;
  right: 24rpx;
}

.status-badge {
  background-color: rgba(16, 185, 129, 0.9);
  color: #fff;
  font-size: 24rpx;
  font-weight: 600;
  padding: 8rpx 20rpx;
  border-radius: 12rpx;
}

/* 信息区 */
.info-section {
  padding: 32rpx;
}

.event-title {
  font-size: 38rpx;
  font-weight: 700;
  color: #f5f5f5;
  margin-bottom: 20rpx;
  line-height: 1.3;
}

.organizer-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 28rpx;
}

.organizer-avatar {
  width: 48rpx;
  height: 48rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-text {
  font-size: 22rpx;
  color: #1a1a2e;
  font-weight: 700;
}

.organizer-name {
  font-size: 26rpx;
  color: #b0b0c0;
}

.official-badge {
  background-color: rgba(246, 195, 66, 0.12);
  border-radius: 6rpx;
  padding: 4rpx 12rpx;
}

.official-text {
  font-size: 20rpx;
  color: #f6c342;
}

.info-items {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.info-row {
  display: flex;
  align-items: flex-start;
  gap: 16rpx;
}

.info-icon {
  font-size: 28rpx;
  margin-top: 4rpx;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.info-label {
  font-size: 22rpx;
  color: #6b6b80;
}

.info-value {
  font-size: 28rpx;
  color: #f5f5f5;
}

.info-value.gold {
  color: #f6c342;
  font-weight: 600;
}

/* 通用区块 */
.section {
  padding: 0 32rpx 32rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: 20rpx;
}

/* 奖金 */
.prize-list {
  background-color: #2a2a3e;
  border-radius: 20rpx;
  padding: 20rpx;
}

.prize-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16rpx 12rpx;
  border-bottom: 1rpx solid #3a3a50;
}

.prize-item:last-child {
  border-bottom: none;
}

.prize-rank {
  font-size: 26rpx;
  color: #b0b0c0;
  font-weight: 500;
}

.prize-rank.gold {
  color: #f6c342;
}

.prize-rank.silver {
  color: #c0c0c0;
}

.prize-rank.bronze {
  color: #cd7f32;
}

.prize-amount {
  font-size: 26rpx;
  color: #f5f5f5;
  font-weight: 500;
}

/* 规则 */
.rules-content {
  background-color: #2a2a3e;
  border-radius: 20rpx;
  padding: 24rpx;
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.rule-text {
  font-size: 26rpx;
  color: #b0b0c0;
  line-height: 1.6;
}

/* 时间安排 */
.schedule-list {
  background-color: #2a2a3e;
  border-radius: 20rpx;
  padding: 20rpx;
}

.schedule-item {
  display: flex;
  align-items: center;
  gap: 24rpx;
  padding: 14rpx 12rpx;
  border-bottom: 1rpx solid #3a3a50;
}

.schedule-item:last-child {
  border-bottom: none;
}

.schedule-time {
  font-size: 26rpx;
  color: #f6c342;
  font-weight: 600;
  min-width: 80rpx;
}

.schedule-event {
  font-size: 26rpx;
  color: #f5f5f5;
}

/* 已报名预览 */
.enrolled-preview {
  display: flex;
  align-items: center;
}

.enrolled-avatar {
  width: 56rpx;
  height: 56rpx;
  background: linear-gradient(135deg, #3a3a50 0%, #2a2a3e 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: -12rpx;
  border: 2rpx solid #1a1a2e;
}

.enrolled-text {
  font-size: 22rpx;
  color: #f5f5f5;
}

.enrolled-more {
  width: 56rpx;
  height: 56rpx;
  background-color: #3a3a50;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 4rpx;
}

.more-text {
  font-size: 18rpx;
  color: #b0b0c0;
}

/* 底部操作栏 */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  padding: 20rpx 32rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  background-color: #1a1a2e;
  border-top: 1rpx solid #3a3a50;
}

.price-info {
  display: flex;
  flex-direction: column;
  margin-right: 32rpx;
}

.price-label {
  font-size: 22rpx;
  color: #6b6b80;
}

.price-value {
  font-size: 36rpx;
  font-weight: 700;
  color: #f6c342;
}

.enroll-btn {
  flex: 1;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 16rpx;
  padding: 26rpx;
  text-align: center;
}

.enroll-text {
  font-size: 30rpx;
  color: #1a1a2e;
  font-weight: 700;
}
</style>
