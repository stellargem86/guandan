<template>
  <view class="page">
    <!-- 俱乐部信息头 -->
    <view class="club-header-card">
      <view class="club-avatar">
        <text class="avatar-text">南</text>
      </view>
      <view class="club-basic">
        <text class="club-name">南京掼蛋联盟</text>
        <text class="club-id">ID: 10001</text>
      </view>
    </view>

    <!-- 管理菜单 -->
    <view class="menu-section">
      <view class="menu-item" v-for="item in menuItems" :key="item.title" @tap="handleMenu(item)">
        <view class="menu-left">
          <text class="menu-icon">{{ item.icon }}</text>
          <text class="menu-title">{{ item.title }}</text>
        </view>
        <view class="menu-right">
          <text class="menu-badge" v-if="item.badge">{{ item.badge }}</text>
          <text class="menu-arrow">›</text>
        </view>
      </view>
    </view>

    <!-- 成员申请管理 -->
    <view class="section-card">
      <text class="section-title">会员内部审计</text>
      <view class="apply-list">
        <view class="apply-item" v-for="apply in applyList" :key="apply.id">
          <view class="apply-avatar">
            <text class="apply-char">{{ apply.name.charAt(0) }}</text>
          </view>
          <view class="apply-info">
            <text class="apply-name">{{ apply.name }}</text>
            <text class="apply-desc">{{ apply.desc }}</text>
          </view>
          <view class="apply-actions">
            <view class="approve-btn" @tap="handleApprove(apply)">
              <text class="approve-text">通过</text>
            </view>
            <view class="reject-btn" @tap="handleReject(apply)">
              <text class="reject-text">拒绝</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 快捷操作 -->
    <view class="section-card">
      <text class="section-title">快捷操作</text>
      <view class="quick-actions">
        <view class="quick-action-item" @tap="goEvent">
          <text class="quick-icon">📅</text>
          <text class="quick-label">发布活动</text>
        </view>
        <view class="quick-action-item" @tap="goNotice">
          <text class="quick-icon">📢</text>
          <text class="quick-label">发布公告</text>
        </view>
        <view class="quick-action-item" @tap="goMembers">
          <text class="quick-icon">👥</text>
          <text class="quick-label">成员管理</text>
        </view>
        <view class="quick-action-item" @tap="goSettings">
          <text class="quick-icon">⚙️</text>
          <text class="quick-label">俱乐部设置</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const menuItems = ref([
  { icon: '📢', title: '俱乐部聊天', badge: '3', action: 'chat' },
  { icon: '📋', title: '牌友互通有无', badge: '', action: 'exchange' },
  { icon: '🏆', title: '俱乐部活动', badge: '2', action: 'events' },
  { icon: '👥', title: '会员内部审计', badge: '5', action: 'audit' },
])

const applyList = ref([
  { id: '1', name: '赵掼友', desc: '想加入你的俱乐部？' },
  { id: '2', name: '钱小姐', desc: '是否有报名资格？' },
])

function handleMenu(item: any) {
  uni.showToast({ title: `打开: ${item.title}`, icon: 'none' })
}

function handleApprove(apply: any) {
  uni.showToast({ title: `已通过 ${apply.name}`, icon: 'success' })
}

function handleReject(apply: any) {
  uni.showToast({ title: `已拒绝 ${apply.name}`, icon: 'none' })
}

function goEvent() {
  uni.showToast({ title: '发布活动', icon: 'none' })
}

function goNotice() {
  uni.showToast({ title: '发布公告', icon: 'none' })
}

function goMembers() {
  uni.navigateTo({ url: '/pages/clubs/members' })
}

function goSettings() {
  uni.showToast({ title: '俱乐部设置', icon: 'none' })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
}

/* 头部卡片 */
.club-header-card {
  display: flex;
  align-items: center;
  background-color: #FFFFFF;
  padding: 32rpx 24rpx;
  gap: 20rpx;
  margin-bottom: 16rpx;
}

.club-avatar {
  width: 96rpx;
  height: 96rpx;
  background-color: #C41E3A;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-text {
  font-size: 40rpx;
  color: #FFFFFF;
  font-weight: 700;
}

.club-basic {
  flex: 1;
}

.club-name {
  font-size: 32rpx;
  font-weight: 700;
  color: #333333;
  margin-bottom: 4rpx;
}

.club-id {
  font-size: 24rpx;
  color: #999999;
}

/* 菜单 */
.menu-section {
  background-color: #FFFFFF;
  margin-bottom: 16rpx;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28rpx 24rpx;
  border-bottom: 1rpx solid #F5F5F5;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-left {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.menu-icon {
  font-size: 32rpx;
}

.menu-title {
  font-size: 28rpx;
  color: #333333;
}

.menu-right {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.menu-badge {
  font-size: 22rpx;
  color: #FFFFFF;
  background-color: #C41E3A;
  border-radius: 20rpx;
  padding: 2rpx 12rpx;
  min-width: 32rpx;
  text-align: center;
}

.menu-arrow {
  font-size: 28rpx;
  color: #CCCCCC;
}

/* 通用卡片 */
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

/* 申请列表 */
.apply-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.apply-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 16rpx;
  background-color: #FAFAFA;
  border-radius: 12rpx;
}

.apply-avatar {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  background-color: #FFF0F0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.apply-char {
  font-size: 24rpx;
  color: #C41E3A;
  font-weight: 600;
}

.apply-info {
  flex: 1;
}

.apply-name {
  font-size: 28rpx;
  color: #333333;
  font-weight: 500;
}

.apply-desc {
  font-size: 22rpx;
  color: #999999;
  margin-top: 4rpx;
}

.apply-actions {
  display: flex;
  gap: 12rpx;
}

.approve-btn {
  background-color: #C41E3A;
  border-radius: 20rpx;
  padding: 8rpx 20rpx;
}

.approve-text {
  font-size: 22rpx;
  color: #FFFFFF;
}

.reject-btn {
  border: 1rpx solid #E0E0E0;
  border-radius: 20rpx;
  padding: 8rpx 20rpx;
}

.reject-text {
  font-size: 22rpx;
  color: #999999;
}

/* 快捷操作 */
.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.quick-action-item {
  width: calc(50% - 8rpx);
  display: flex;
  align-items: center;
  gap: 12rpx;
  padding: 20rpx;
  background-color: #FAFAFA;
  border-radius: 12rpx;
}

.quick-icon {
  font-size: 32rpx;
}

.quick-label {
  font-size: 26rpx;
  color: #333333;
}
</style>
