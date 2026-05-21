<template>
  <view class="page">
    <view class="form-container">
      <!-- 标题 -->
      <view class="form-group">
        <text class="form-label">组局标题</text>
        <input
          class="form-input"
          v-model="form.title"
          placeholder="例：商务精英掼蛋局"
          placeholder-class="input-placeholder"
        />
      </view>

      <!-- 时间 -->
      <view class="form-group">
        <text class="form-label">开始时间</text>
        <picker mode="date" @change="onDateChange">
          <view class="form-picker">
            <text class="picker-text" :class="{ placeholder: !form.date }">
              {{ form.date || '请选择日期' }}
            </text>
            <text class="picker-arrow">›</text>
          </view>
        </picker>
        <picker mode="time" @change="onTimeChange">
          <view class="form-picker" style="margin-top: 16rpx;">
            <text class="picker-text" :class="{ placeholder: !form.time }">
              {{ form.time || '请选择时间' }}
            </text>
            <text class="picker-arrow">›</text>
          </view>
        </picker>
      </view>

      <!-- 地点 -->
      <view class="form-group">
        <text class="form-label">牌局地点</text>
        <input
          class="form-input"
          v-model="form.location"
          placeholder="例：金陵棋牌会所 VIP3"
          placeholder-class="input-placeholder"
        />
      </view>

      <!-- 段位要求 -->
      <view class="form-group">
        <text class="form-label">段位要求</text>
        <picker :range="levelOptions" @change="onLevelChange">
          <view class="form-picker">
            <text class="picker-text" :class="{ placeholder: !form.level }">
              {{ form.level || '请选择段位要求' }}
            </text>
            <text class="picker-arrow">›</text>
          </view>
        </picker>
      </view>

      <!-- 行业标签 -->
      <view class="form-group">
        <text class="form-label">行业标签</text>
        <picker :range="industryOptions" @change="onIndustryChange">
          <view class="form-picker">
            <text class="picker-text" :class="{ placeholder: !form.industry }">
              {{ form.industry || '请选择行业（可选）' }}
            </text>
            <text class="picker-arrow">›</text>
          </view>
        </picker>
      </view>

      <!-- 人数 -->
      <view class="form-group">
        <text class="form-label">需要人数</text>
        <view class="number-selector">
          <view class="num-btn" @tap="decreaseCount">
            <text class="num-btn-text">-</text>
          </view>
          <text class="num-value">{{ form.playerCount }}</text>
          <view class="num-btn" @tap="increaseCount">
            <text class="num-btn-text">+</text>
          </view>
        </view>
      </view>

      <!-- 押金 -->
      <view class="form-group">
        <text class="form-label">押金金额（元）</text>
        <input
          class="form-input"
          v-model="form.deposit"
          type="number"
          placeholder="0 表示无押金"
          placeholder-class="input-placeholder"
        />
      </view>

      <!-- 备注 -->
      <view class="form-group">
        <text class="form-label">补充说明</text>
        <textarea
          class="form-textarea"
          v-model="form.remark"
          placeholder="例：结束后可一起聚餐，费用AA"
          placeholder-class="input-placeholder"
        />
      </view>
    </view>

    <!-- 提交按钮 -->
    <view class="submit-area">
      <view class="submit-btn" @tap="handleSubmit">
        <text class="submit-text">发布组局</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const levelOptions = ['不限', 'B段位以上', 'A段位以上', 'A+段位以上', 'S段位']
const industryOptions = ['不限', '金融', '互联网', '教育', '地产', '医疗', '法律', '制造']

const form = ref({
  title: '',
  date: '',
  time: '',
  location: '',
  level: '',
  industry: '',
  playerCount: 3,
  deposit: '',
  remark: '',
})

function onDateChange(e: any) {
  form.value.date = e.detail.value
}

function onTimeChange(e: any) {
  form.value.time = e.detail.value
}

function onLevelChange(e: any) {
  form.value.level = levelOptions[e.detail.value]
}

function onIndustryChange(e: any) {
  form.value.industry = industryOptions[e.detail.value]
}

function increaseCount() {
  if (form.value.playerCount < 7) form.value.playerCount++
}

function decreaseCount() {
  if (form.value.playerCount > 1) form.value.playerCount--
}

function handleSubmit() {
  if (!form.value.title) {
    uni.showToast({ title: '请输入组局标题', icon: 'none' })
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
  padding-bottom: 160rpx;
}

.form-container {
  padding: 32rpx;
}

.form-group {
  margin-bottom: 32rpx;
}

.form-label {
  font-size: 28rpx;
  color: #f5f5f5;
  font-weight: 500;
  margin-bottom: 16rpx;
  display: block;
}

.form-input {
  width: 100%;
  height: 88rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
  color: #f5f5f5;
  border: 1rpx solid #3a3a50;
}

.form-textarea {
  width: 100%;
  height: 200rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  padding: 24rpx;
  font-size: 28rpx;
  color: #f5f5f5;
  border: 1rpx solid #3a3a50;
}

.input-placeholder {
  color: #6b6b80;
}

.form-picker {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 88rpx;
  background-color: #2a2a3e;
  border-radius: 16rpx;
  padding: 0 24rpx;
  border: 1rpx solid #3a3a50;
}

.picker-text {
  font-size: 28rpx;
  color: #f5f5f5;
}

.picker-text.placeholder {
  color: #6b6b80;
}

.picker-arrow {
  font-size: 32rpx;
  color: #6b6b80;
}

/* 人数选择器 */
.number-selector {
  display: flex;
  align-items: center;
  gap: 32rpx;
}

.num-btn {
  width: 72rpx;
  height: 72rpx;
  background-color: #2a2a3e;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1rpx solid #3a3a50;
}

.num-btn-text {
  font-size: 36rpx;
  color: #f6c342;
  font-weight: 600;
}

.num-value {
  font-size: 40rpx;
  font-weight: 700;
  color: #f6c342;
  min-width: 60rpx;
  text-align: center;
}

/* 提交按钮 */
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
