<template>
  <view class="page">
    <view class="form-container">
      <!-- 内容输入 -->
      <textarea
        class="content-input"
        v-model="content"
        placeholder="分享你的掼蛋心得、约局信息、战报..."
        placeholder-class="input-placeholder"
        :maxlength="500"
        auto-height
      />

      <!-- 字数统计 -->
      <view class="char-count">
        <text class="char-text">{{ content.length }}/500</text>
      </view>

      <!-- 图片上传区域 -->
      <view class="image-section">
        <text class="section-label">添加图片</text>
        <view class="image-grid">
          <view class="image-item" v-for="(img, idx) in images" :key="idx">
            <view class="image-preview">
              <text class="img-emoji">{{ img }}</text>
            </view>
            <view class="remove-btn" @tap="removeImage(idx)">
              <text class="remove-text">×</text>
            </view>
          </view>
          <view class="image-add" @tap="addImage" v-if="images.length < 9">
            <text class="add-icon">+</text>
            <text class="add-text">添加</text>
          </view>
        </view>
      </view>

      <!-- 标签选择 -->
      <view class="tag-section">
        <text class="section-label">选择标签</text>
        <view class="tag-list">
          <view
            class="tag-item"
            :class="{ active: selectedTag === tag }"
            v-for="tag in tagOptions"
            :key="tag"
            @tap="selectedTag = tag"
          >
            <text class="tag-item-text" :class="{ active: selectedTag === tag }">{{ tag }}</text>
          </view>
        </view>
      </view>

      <!-- 位置 -->
      <view class="location-section" @tap="selectLocation">
        <text class="location-icon">📍</text>
        <text class="location-text">{{ location || '添加位置（可选）' }}</text>
        <text class="location-arrow">›</text>
      </view>
    </view>

    <!-- 发布按钮 -->
    <view class="submit-area">
      <view class="submit-btn" @tap="handlePublish">
        <text class="submit-text">发布</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const content = ref('')
const images = ref<string[]>([])
const selectedTag = ref('')
const location = ref('')

const tagOptions = ['约局', '战报', '心得', '推荐', '求组', '其他']

function addImage() {
  if (images.value.length < 9) {
    const emojis = ['📷', '🎴', '🃏', '🏆', '🎯', '📊', '🎮', '🀄', '🎲']
    images.value.push(emojis[images.value.length % emojis.length])
  }
}

function removeImage(idx: number) {
  images.value.splice(idx, 1)
}

function selectLocation() {
  location.value = '南京市·建邺区'
}

function handlePublish() {
  if (!content.value.trim()) {
    uni.showToast({ title: '请输入内容', icon: 'none' })
    return
  }
  uni.showToast({ title: '发布成功！', icon: 'success' })
  setTimeout(() => {
    uni.navigateBack()
  }, 1500)
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  padding-bottom: 140rpx;
}

.form-container {
  padding: 32rpx;
}

.content-input {
  width: 100%;
  min-height: 300rpx;
  background-color: #2a2a3e;
  border-radius: 20rpx;
  padding: 28rpx;
  font-size: 30rpx;
  color: #f5f5f5;
  line-height: 1.6;
}

.input-placeholder {
  color: #6b6b80;
}

.char-count {
  display: flex;
  justify-content: flex-end;
  padding: 12rpx 0;
}

.char-text {
  font-size: 22rpx;
  color: #6b6b80;
}

/* 图片区域 */
.image-section {
  margin-top: 32rpx;
}

.section-label {
  font-size: 28rpx;
  color: #f5f5f5;
  font-weight: 500;
  margin-bottom: 16rpx;
  display: block;
}

.image-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.image-item {
  position: relative;
  width: 200rpx;
  height: 200rpx;
}

.image-preview {
  width: 100%;
  height: 100%;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1rpx solid #3a3a50;
}

.img-emoji {
  font-size: 56rpx;
}

.remove-btn {
  position: absolute;
  top: -10rpx;
  right: -10rpx;
  width: 40rpx;
  height: 40rpx;
  background-color: #ef4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-text {
  font-size: 24rpx;
  color: #fff;
  font-weight: 700;
}

.image-add {
  width: 200rpx;
  height: 200rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2rpx dashed #3a3a50;
}

.add-icon {
  font-size: 48rpx;
  color: #6b6b80;
}

.add-text {
  font-size: 22rpx;
  color: #6b6b80;
  margin-top: 8rpx;
}

/* 标签 */
.tag-section {
  margin-top: 32rpx;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.tag-item {
  padding: 14rpx 28rpx;
  background-color: #2a2a3e;
  border-radius: 32rpx;
  border: 1rpx solid #3a3a50;
}

.tag-item.active {
  background-color: rgba(246, 195, 66, 0.12);
  border-color: #f6c342;
}

.tag-item-text {
  font-size: 26rpx;
  color: #b0b0c0;
}

.tag-item-text.active {
  color: #f6c342;
}

/* 位置 */
.location-section {
  display: flex;
  align-items: center;
  padding: 24rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  margin-top: 32rpx;
}

.location-icon {
  font-size: 28rpx;
  margin-right: 12rpx;
}

.location-text {
  flex: 1;
  font-size: 28rpx;
  color: #b0b0c0;
}

.location-arrow {
  font-size: 32rpx;
  color: #6b6b80;
}

/* 发布按钮 */
.submit-area {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 24rpx 32rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  background-color: #1a1a2e;
}

.submit-btn {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 16rpx;
  padding: 28rpx;
  text-align: center;
}

.submit-text {
  font-size: 32rpx;
  color: #1a1a2e;
  font-weight: 700;
}
</style>
