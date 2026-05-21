<template>
  <view class="page">
    <!-- 俱乐部头部 -->
    <view class="club-header">
      <view class="header-bg"></view>
      <view class="header-content">
        <view class="club-avatar">
          <text class="avatar-text">南</text>
        </view>
        <text class="club-name">南京掼蛋联盟</text>
        <text class="club-id">ID: 10001</text>
      </view>
    </view>

    <!-- 导航Tab -->
    <view class="nav-tabs">
      <view
        class="nav-tab"
        :class="{ active: activeNav === tab.value }"
        v-for="tab in navTabs"
        :key="tab.value"
        @tap="activeNav = tab.value"
      >
        <text class="nav-tab-text" :class="{ active: activeNav === tab.value }">{{ tab.label }}</text>
      </view>
    </view>

    <!-- 数据统计 -->
    <view class="stats-card" v-if="activeNav === 'info'">
      <view class="stats-row">
        <view class="stat-item">
          <text class="stat-value">128</text>
          <text class="stat-label">成员</text>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item">
          <text class="stat-value">36</text>
          <text class="stat-label">活跃</text>
        </view>
      </view>
    </view>

    <!-- 俱乐部介绍 -->
    <view class="section-card" v-if="activeNav === 'info'">
      <text class="desc-text">
        掼蛋兴趣爱好相同的朋友组织机构，提供友互竞技掼蛋服务的长期性组织。俱乐部致力于为牌友提供高品质的竞技环境和社交平台。
      </text>
    </view>

    <!-- 俱乐部聊天入口 -->
    <view class="section-card chat-section" v-if="activeNav === 'info'">
      <text class="section-title">俱乐部聊天</text>
      <view class="chat-list">
        <view class="chat-item">
          <view class="chat-avatar">
            <text class="chat-avatar-text">牌</text>
          </view>
          <view class="chat-content">
            <text class="chat-name">牌友互通有无</text>
            <text class="chat-msg">今晚有人组局吗？</text>
          </view>
          <text class="chat-time">16:30</text>
        </view>
        <view class="chat-item">
          <view class="chat-avatar">
            <text class="chat-avatar-text">赛</text>
          </view>
          <view class="chat-content">
            <text class="chat-name">赛板了石</text>
            <text class="chat-msg">明天比赛报名截止</text>
          </view>
          <text class="chat-time">15:20</text>
        </view>
      </view>
    </view>

    <!-- 俱乐部活动 -->
    <view class="section-card" v-if="activeNav === 'activity'">
      <text class="section-title">俱乐部活动</text>
      <view class="activity-list">
        <view class="activity-item" v-for="act in activities" :key="act.id">
          <view class="activity-dot" :class="act.statusClass"></view>
          <view class="activity-info">
            <text class="activity-title">{{ act.title }}</text>
            <text class="activity-desc">{{ act.desc }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 成员列表 -->
    <view class="section-card" v-if="activeNav === 'members'">
      <text class="section-title">俱乐部成员</text>
      <view class="member-list">
        <view class="member-item" v-for="m in members" :key="m.id">
          <view class="member-avatar">
            <text class="member-char">{{ m.name.charAt(0) }}</text>
          </view>
          <view class="member-info">
            <text class="member-name">{{ m.name }}</text>
            <text class="member-role">{{ m.role }}</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部操作 -->
    <view class="bottom-bar">
      <view class="apply-btn" @tap="handleApply">
        <text class="apply-text">申请加入</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeNav = ref('info')

const navTabs = [
  { label: '公告', value: 'info' },
  { label: '活动', value: 'activity' },
  { label: '成员', value: 'members' },
  { label: '战绩', value: 'records' },
]

const activities = ref([
  { id: '1', title: '周末友谊赛', desc: '本周六14:00', statusClass: 'active' },
  { id: '2', title: '月度积分赛', desc: '下周一20:00', statusClass: 'upcoming' },
  { id: '3', title: '新人欢迎赛', desc: '已结束', statusClass: 'done' },
])

const members = ref([
  { id: '1', name: '张会长', role: '会长' },
  { id: '2', name: '李副会', role: '副会长' },
  { id: '3', name: '王秘书', role: '秘书' },
  { id: '4', name: '赵教练', role: '成员' },
  { id: '5', name: '陈掼友', role: '成员' },
])

function handleApply() {
  uni.showToast({ title: '申请已发送', icon: 'success' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding-bottom: 140rpx;
}

/* 头部 */
.club-header {
  position: relative;
}

.header-bg {
  height: 200rpx;
  background: linear-gradient(135deg, #C41E3A 0%, #A01830 100%);
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
  background-color: #C41E3A;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 6rpx solid #FFFFFF;
  margin-bottom: 12rpx;
}

.avatar-text {
  font-size: 48rpx;
  color: #FFFFFF;
  font-weight: 700;
}

.club-name {
  font-size: 34rpx;
  font-weight: 700;
  color: #333333;
  margin-bottom: 4rpx;
}

.club-id {
  font-size: 24rpx;
  color: #999999;
}

/* 导航Tab */
.nav-tabs {
  display: flex;
  background-color: #FFFFFF;
  margin-top: 24rpx;
  padding: 0 24rpx;
  border-bottom: 1rpx solid #F0F0F0;
}

.nav-tab {
  padding: 20rpx 24rpx;
}

.nav-tab.active {
  border-bottom: 4rpx solid #C41E3A;
}

.nav-tab-text {
  font-size: 28rpx;
  color: #999999;
}

.nav-tab-text.active {
  color: #C41E3A;
  font-weight: 600;
}

/* 统计 */
.stats-card {
  background-color: #FFFFFF;
  margin: 16rpx 24rpx;
  border-radius: 16rpx;
  padding: 24rpx;
}

.stats-row {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6rpx;
}

.stat-value {
  font-size: 36rpx;
  font-weight: 700;
  color: #333333;
}

.stat-label {
  font-size: 24rpx;
  color: #999999;
}

.stat-divider {
  width: 1rpx;
  height: 48rpx;
  background-color: #F0F0F0;
}

/* 通用区块 */
.section-card {
  background-color: #FFFFFF;
  margin: 16rpx 24rpx;
  border-radius: 16rpx;
  padding: 24rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 16rpx;
}

.desc-text {
  font-size: 26rpx;
  color: #666666;
  line-height: 1.8;
}

/* 聊天列表 */
.chat-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.chat-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.chat-avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  background-color: #FFF0F0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-avatar-text {
  font-size: 26rpx;
  color: #C41E3A;
  font-weight: 600;
}

.chat-content {
  flex: 1;
}

.chat-name {
  font-size: 28rpx;
  color: #333333;
  font-weight: 500;
  margin-bottom: 4rpx;
}

.chat-msg {
  font-size: 24rpx;
  color: #999999;
}

.chat-time {
  font-size: 22rpx;
  color: #CCCCCC;
}

/* 活动列表 */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 16rpx;
  background-color: #FAFAFA;
  border-radius: 12rpx;
}

.activity-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  flex-shrink: 0;
}

.activity-dot.active {
  background-color: #4CAF50;
}

.activity-dot.upcoming {
  background-color: #FF9800;
}

.activity-dot.done {
  background-color: #CCCCCC;
}

.activity-info {
  flex: 1;
}

.activity-title {
  font-size: 28rpx;
  color: #333333;
  font-weight: 500;
}

.activity-desc {
  font-size: 24rpx;
  color: #999999;
  margin-top: 4rpx;
}

/* 成员列表 */
.member-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.member-avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  background-color: #FFF0F0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.member-char {
  font-size: 24rpx;
  color: #C41E3A;
  font-weight: 600;
}

.member-info {
  flex: 1;
}

.member-name {
  font-size: 28rpx;
  color: #333333;
}

.member-role {
  font-size: 22rpx;
  color: #999999;
}

/* 底部操作 */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20rpx 24rpx;
  padding-bottom: calc(20rpx + env(safe-area-inset-bottom));
  background-color: #FFFFFF;
  border-top: 1rpx solid #F0F0F0;
}

.apply-btn {
  background-color: #C41E3A;
  border-radius: 40rpx;
  padding: 24rpx;
  text-align: center;
}

.apply-text {
  font-size: 30rpx;
  color: #FFFFFF;
  font-weight: 600;
}
</style>
