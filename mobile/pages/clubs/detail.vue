<template>
  <view class="page">
    <!-- 俱乐部头部 -->
    <view class="club-header">
      <view class="header-bg"></view>
      <view class="header-content">
        <view class="club-avatar">
          <text class="avatar-emoji">🏆</text>
        </view>
        <text class="club-name">金陵掼蛋俱乐部</text>
        <text class="club-id">ID: GD-NJ-001</text>
      </view>
    </view>

    <!-- 数据统计 -->
    <view class="stats-row">
      <view class="stat-item">
        <text class="stat-value">128</text>
        <text class="stat-label">成员</text>
      </view>
      <view class="stat-divider"></view>
      <view class="stat-item">
        <text class="stat-value">98</text>
        <text class="stat-label">活跃</text>
      </view>
      <view class="stat-divider"></view>
      <view class="stat-item">
        <text class="stat-value gold">2680</text>
        <text class="stat-label">ELO均分</text>
      </view>
      <view class="stat-divider"></view>
      <view class="stat-item">
        <text class="stat-value">36</text>
        <text class="stat-label">本月赛事</text>
      </view>
    </view>

    <!-- 俱乐部简介 -->
    <view class="section">
      <text class="section-title">俱乐部简介</text>
      <view class="section-card">
        <text class="desc-text">
          金陵掼蛋俱乐部成立于2022年，是南京地区最活跃的掼蛋竞技社群之一。俱乐部汇聚了来自金融、科技、教育等多个行业的精英牌友，定期举办俱乐部内部赛事和跨俱乐部对抗赛。我们崇尚"以牌会友、以技交心"的理念，致力于打造高品质的掼蛋社交圈。
        </text>
      </view>
    </view>

    <!-- 俱乐部管理层 -->
    <view class="section">
      <text class="section-title">管理团队</text>
      <view class="admin-list">
        <view class="admin-item" v-for="admin in admins" :key="admin.name">
          <view class="admin-avatar">
            <text class="admin-avatar-text">{{ admin.avatar }}</text>
          </view>
          <view class="admin-info">
            <text class="admin-name">{{ admin.name }}</text>
            <text class="admin-role">{{ admin.role }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 俱乐部活动 -->
    <view class="section">
      <text class="section-title">俱乐部活动</text>
      <view class="activity-list">
        <view class="activity-item" v-for="activity in activities" :key="activity.id">
          <view class="activity-date">
            <text class="date-day">{{ activity.day }}</text>
            <text class="date-month">{{ activity.month }}</text>
          </view>
          <view class="activity-info">
            <text class="activity-title">{{ activity.title }}</text>
            <text class="activity-desc">{{ activity.desc }}</text>
          </view>
          <view class="activity-status" :class="activity.statusClass">
            <text class="status-text">{{ activity.status }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 成员预览 -->
    <view class="section">
      <view class="section-header-row">
        <text class="section-title">俱乐部成员</text>
        <text class="section-more" @tap="goMembers">查看全部 ›</text>
      </view>
      <view class="member-preview">
        <view class="member-avatar" v-for="(m, idx) in memberPreview" :key="idx">
          <text class="member-text">{{ m }}</text>
        </view>
        <view class="member-more">
          <text class="more-text">+120</text>
        </view>
      </view>
    </view>

    <!-- 底部操作 -->
    <view class="bottom-bar">
      <view class="chat-btn" @tap="goChat">
        <text class="chat-icon">💬</text>
        <text class="chat-text">俱乐部聊天</text>
      </view>
      <view class="action-btn" @tap="handleJoin">
        <text class="action-text">申请加入</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const admins = ref([
  { avatar: '张', name: '张会长', role: '会长' },
  { avatar: '李', name: '李副会', role: '副会长' },
  { avatar: '王', name: '王秘书', role: '秘书长' },
])

const activities = ref([
  {
    id: '1',
    day: '15',
    month: '3月',
    title: '周五晚间积分赛',
    desc: '本周五20:00，金陵会所VIP厅',
    status: '报名中',
    statusClass: 'enrolling',
  },
  {
    id: '2',
    day: '18',
    month: '3月',
    title: '跨俱乐部友谊赛',
    desc: '对阵龙虎山精英会，4v4',
    status: '即将开始',
    statusClass: 'upcoming',
  },
  {
    id: '3',
    day: '22',
    month: '3月',
    title: '新成员欢迎赛',
    desc: '欢迎新加入的8位牌友',
    status: '筹备中',
    statusClass: 'preparing',
  },
  {
    id: '4',
    day: '10',
    month: '3月',
    title: '月度冠军争霸赛',
    desc: '恭喜陈总夺得本月冠军',
    status: '已结束',
    statusClass: 'finished',
  },
])

const memberPreview = ref(['张', '李', '王', '陈', '刘', '赵', '周', '吴'])

function goMembers() {
  uni.navigateTo({ url: '/pages/clubs/members' })
}

function goChat() {
  uni.navigateTo({ url: '/pages/clubs/chat' })
}

function handleJoin() {
  uni.showToast({ title: '申请已发送', icon: 'success' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 140rpx;
}

/* 头部 */
.club-header {
  position: relative;
  padding-bottom: 32rpx;
}

.header-bg {
  height: 200rpx;
  background: linear-gradient(135deg, #2a2a3e 0%, #32324a 50%, #1e1e32 100%);
}

.header-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: -60rpx;
}

.club-avatar {
  width: 120rpx;
  height: 120rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 28rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4rpx solid #1a1a2e;
  margin-bottom: 16rpx;
}

.avatar-emoji {
  font-size: 56rpx;
}

.club-name {
  font-size: 36rpx;
  font-weight: 700;
  color: #f5f5f5;
  margin-bottom: 8rpx;
}

.club-id {
  font-size: 24rpx;
  color: #6b6b80;
}

/* 数据统计 */
.stats-row {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 28rpx 32rpx;
  margin: 24rpx 32rpx;
  background-color: #2a2a3e;
  border-radius: 20rpx;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6rpx;
}

.stat-value {
  font-size: 32rpx;
  font-weight: 700;
  color: #f5f5f5;
}

.stat-value.gold {
  color: #f6c342;
}

.stat-label {
  font-size: 22rpx;
  color: #6b6b80;
}

.stat-divider {
  width: 1rpx;
  height: 48rpx;
  background-color: #3a3a50;
}

/* 通用区块 */
.section {
  padding: 0 32rpx 32rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #f5f5f5;
  margin-bottom: 16rpx;
}

.section-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16rpx;
}

.section-more {
  font-size: 24rpx;
  color: #f6c342;
}

.section-card {
  background-color: #2a2a3e;
  border-radius: 16rpx;
  padding: 24rpx;
}

.desc-text {
  font-size: 26rpx;
  color: #b0b0c0;
  line-height: 1.8;
}

/* 管理层 */
.admin-list {
  display: flex;
  gap: 24rpx;
}

.admin-item {
  display: flex;
  align-items: center;
  gap: 12rpx;
  background-color: #2a2a3e;
  border-radius: 12rpx;
  padding: 16rpx 20rpx;
}

.admin-avatar {
  width: 48rpx;
  height: 48rpx;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.admin-avatar-text {
  font-size: 20rpx;
  color: #1a1a2e;
  font-weight: 700;
}

.admin-info {
  display: flex;
  flex-direction: column;
}

.admin-name {
  font-size: 24rpx;
  color: #f5f5f5;
}

.admin-role {
  font-size: 20rpx;
  color: #f6c342;
}

/* 活动列表 */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 20rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
}

.activity-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 80rpx;
  margin-right: 20rpx;
}

.date-day {
  font-size: 32rpx;
  font-weight: 700;
  color: #f6c342;
}

.date-month {
  font-size: 20rpx;
  color: #6b6b80;
}

.activity-info {
  flex: 1;
}

.activity-title {
  font-size: 26rpx;
  color: #f5f5f5;
  font-weight: 500;
  margin-bottom: 4rpx;
}

.activity-desc {
  font-size: 22rpx;
  color: #6b6b80;
}

.activity-status {
  padding: 6rpx 14rpx;
  border-radius: 8rpx;
  flex-shrink: 0;
}

.activity-status.enrolling {
  background-color: rgba(16, 185, 129, 0.12);
}

.activity-status.upcoming {
  background-color: rgba(59, 130, 246, 0.12);
}

.activity-status.preparing {
  background-color: rgba(246, 195, 66, 0.12);
}

.activity-status.finished {
  background-color: rgba(107, 107, 128, 0.12);
}

.status-text {
  font-size: 20rpx;
  color: #10b981;
}

.activity-status.upcoming .status-text {
  color: #3b82f6;
}

.activity-status.preparing .status-text {
  color: #f6c342;
}

.activity-status.finished .status-text {
  color: #6b6b80;
}

/* 成员预览 */
.member-preview {
  display: flex;
  align-items: center;
}

.member-avatar {
  width: 56rpx;
  height: 56rpx;
  background: linear-gradient(135deg, #3a3a50 0%, #2a2a3e 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: -10rpx;
  border: 2rpx solid #1a1a2e;
}

.member-text {
  font-size: 22rpx;
  color: #f5f5f5;
}

.member-more {
  width: 56rpx;
  height: 56rpx;
  background-color: #3a3a50;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 8rpx;
}

.more-text {
  font-size: 18rpx;
  color: #b0b0c0;
}

/* 底部操作 */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: 16rpx;
  padding: 20rpx 32rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  background-color: #1a1a2e;
  border-top: 1rpx solid #3a3a50;
}

.chat-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  padding: 24rpx 32rpx;
  border: 1rpx solid rgba(246, 195, 66, 0.5);
  border-radius: 16rpx;
}

.chat-icon {
  font-size: 28rpx;
}

.chat-text {
  font-size: 26rpx;
  color: #f6c342;
}

.action-btn {
  flex: 1;
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 16rpx;
  padding: 24rpx;
  text-align: center;
}

.action-text {
  font-size: 30rpx;
  color: #1a1a2e;
  font-weight: 700;
}
</style>
