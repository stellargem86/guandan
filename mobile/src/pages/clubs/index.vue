<template>
  <view class="page">
    <!-- 搜索栏 -->
    <view class="search-section">
      <view class="search-bar">
        <text class="search-icon">🔍</text>
        <input class="search-input" placeholder="搜索俱乐部名称" placeholder-class="placeholder" v-model="searchText" />
      </view>
    </view>

    <!-- 俱乐部列表 -->
    <scroll-view scroll-y class="club-scroll">
      <view class="club-card" v-for="club in clubs" :key="club.id" @tap="goDetail(club.id)">
        <view class="club-avatar">
          <image v-if="club.avatar" :src="club.avatar" class="avatar-img" mode="aspectFill" />
          <view v-else class="avatar-placeholder">
            <text class="avatar-text">{{ club.name.charAt(0) }}</text>
          </view>
        </view>
        <view class="club-info">
          <view class="club-name-row">
            <text class="club-name">{{ club.name }}</text>
            <view class="club-tag" v-if="club.tag">
              <text class="tag-text">{{ club.tag }}</text>
            </view>
          </view>
          <view class="club-meta">
            <text class="meta-text">👥 {{ club.members }}/{{ club.maxMembers }}</text>
            <text class="meta-text">📍 {{ club.region }}</text>
          </view>
        </view>
        <view class="club-arrow">
          <text class="arrow-icon">›</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const searchText = ref('')

const clubs = ref([
  {
    id: '1',
    name: '南京掼蛋联盟',
    avatar: '',
    tag: '热门',
    members: 128,
    maxMembers: 200,
    region: '南京·建邺',
  },
  {
    id: '2',
    name: '金陵掼蛋俱乐部',
    avatar: '',
    tag: '',
    members: 96,
    maxMembers: 150,
    region: '南京·鼓楼',
  },
  {
    id: '3',
    name: '玄武湖掼蛋俱乐部',
    avatar: '',
    tag: '',
    members: 64,
    maxMembers: 100,
    region: '南京·玄武',
  },
  {
    id: '4',
    name: '企业家掼蛋俱乐部',
    avatar: '',
    tag: '精英',
    members: 156,
    maxMembers: 200,
    region: '南京·秦淮',
  },
])

function goDetail(id: string) {
  uni.navigateTo({ url: `/pages/clubs/detail?id=${id}` })
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #F5F5F5;
  padding-bottom: 120rpx;
}

/* 搜索栏 */
.search-section {
  padding: 16rpx 24rpx;
  background-color: #FFFFFF;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #F5F5F5;
  border-radius: 32rpx;
  padding: 16rpx 24rpx;
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

/* 俱乐部列表 */
.club-scroll {
  height: calc(100vh - 140rpx);
  padding: 16rpx 24rpx;
}

.club-card {
  display: flex;
  align-items: center;
  background-color: #FFFFFF;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.club-avatar {
  width: 96rpx;
  height: 96rpx;
  border-radius: 16rpx;
  margin-right: 20rpx;
  flex-shrink: 0;
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background-color: #C41E3A;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16rpx;
}

.avatar-text {
  font-size: 36rpx;
  color: #FFFFFF;
  font-weight: 700;
}

.club-info {
  flex: 1;
}

.club-name-row {
  display: flex;
  align-items: center;
  gap: 8rpx;
  margin-bottom: 8rpx;
}

.club-name {
  font-size: 30rpx;
  font-weight: 600;
  color: #333333;
}

.club-tag {
  background-color: #FFF0F0;
  border-radius: 6rpx;
  padding: 2rpx 10rpx;
}

.tag-text {
  font-size: 20rpx;
  color: #C41E3A;
}

.club-meta {
  display: flex;
  gap: 16rpx;
}

.meta-text {
  font-size: 24rpx;
  color: #999999;
}

.club-arrow {
  padding-left: 12rpx;
}

.arrow-icon {
  font-size: 32rpx;
  color: #CCCCCC;
}
</style>
