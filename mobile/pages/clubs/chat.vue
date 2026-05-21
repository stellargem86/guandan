<template>
  <view class="page">
    <!-- 聊天消息列表 -->
    <scroll-view scroll-y class="chat-list" :scroll-into-view="scrollToId">
      <view class="chat-date">
        <text class="date-text">今天</text>
      </view>

      <view
        class="message-item"
        :class="{ 'is-self': msg.isSelf }"
        v-for="msg in messages"
        :key="msg.id"
        :id="`msg-${msg.id}`"
      >
        <view class="msg-avatar" v-if="!msg.isSelf">
          <text class="msg-avatar-text">{{ msg.avatar }}</text>
        </view>
        <view class="msg-content">
          <text class="msg-name" v-if="!msg.isSelf">{{ msg.name }}</text>
          <view class="msg-bubble" :class="{ self: msg.isSelf }">
            <text class="msg-text">{{ msg.text }}</text>
          </view>
          <text class="msg-time">{{ msg.time }}</text>
        </view>
        <view class="msg-avatar" v-if="msg.isSelf">
          <text class="msg-avatar-text">我</text>
        </view>
      </view>
    </scroll-view>

    <!-- 输入栏 -->
    <view class="input-bar">
      <input
        class="msg-input"
        v-model="inputText"
        placeholder="输入消息..."
        placeholder-class="input-placeholder"
        @confirm="sendMessage"
      />
      <view class="send-btn" @tap="sendMessage">
        <text class="send-text">发送</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const inputText = ref('')
const scrollToId = ref('msg-8')

const messages = ref([
  { id: '1', avatar: '张', name: '张会长', text: '大家好，本周五晚间积分赛的报名已经开始了，有空的牌友都来参加！', time: '09:30', isSelf: false },
  { id: '2', avatar: '李', name: '李副会', text: '好的会长，我报名！这次一定拿个好名次 💪', time: '09:32', isSelf: false },
  { id: '3', avatar: '我', name: '我', text: '报名+1，周五见！', time: '09:35', isSelf: true },
  { id: '4', avatar: '陈', name: '陈总', text: '我也参加，顺便问下这次还是金陵会所VIP厅吗？', time: '09:38', isSelf: false },
  { id: '5', avatar: '张', name: '张会长', text: '对，老地方。8点开始，大家提前10分钟到，先喝茶聊聊 ☕', time: '09:40', isSelf: false },
  { id: '6', avatar: '王', name: '王秘书', text: '已统计报名人数，目前8人报名，还有4个名额', time: '10:15', isSelf: false },
  { id: '7', avatar: '刘', name: '刘博士', text: '上周的积分榜出来了吗？感觉自己进步不少', time: '10:20', isSelf: false },
  { id: '8', avatar: '张', name: '张会长', text: '积分榜稍后发到群里，刘博士上周表现确实不错，ELO涨了30分 👏', time: '10:22', isSelf: false },
])

function sendMessage() {
  if (!inputText.value.trim()) return
  const newMsg = {
    id: String(messages.value.length + 1),
    avatar: '我',
    name: '我',
    text: inputText.value,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    isSelf: true,
  }
  messages.value.push(newMsg)
  inputText.value = ''
  scrollToId.value = `msg-${newMsg.id}`
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: #1a1a2e;
  display: flex;
  flex-direction: column;
}

.chat-list {
  flex: 1;
  height: calc(100vh - 120rpx);
  padding: 24rpx 32rpx;
}

.chat-date {
  display: flex;
  justify-content: center;
  margin-bottom: 24rpx;
}

.date-text {
  font-size: 22rpx;
  color: #6b6b80;
  background-color: #2a2a3e;
  padding: 6rpx 20rpx;
  border-radius: 16rpx;
}

/* 消息项 */
.message-item {
  display: flex;
  margin-bottom: 24rpx;
  align-items: flex-start;
}

.message-item.is-self {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 64rpx;
  height: 64rpx;
  background: linear-gradient(135deg, #3a3a50 0%, #32324a 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message-item.is-self .msg-avatar {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
}

.msg-avatar-text {
  font-size: 22rpx;
  color: #f5f5f5;
  font-weight: 600;
}

.message-item.is-self .msg-avatar-text {
  color: #1a1a2e;
}

.msg-content {
  margin: 0 16rpx;
  max-width: 65%;
}

.msg-name {
  font-size: 22rpx;
  color: #6b6b80;
  margin-bottom: 6rpx;
}

.msg-bubble {
  background-color: #2a2a3e;
  border-radius: 20rpx;
  padding: 18rpx 24rpx;
  border-top-left-radius: 4rpx;
}

.msg-bubble.self {
  background: linear-gradient(135deg, rgba(246, 195, 66, 0.15) 0%, rgba(212, 165, 55, 0.1) 100%);
  border-top-left-radius: 20rpx;
  border-top-right-radius: 4rpx;
  border: 1rpx solid rgba(246, 195, 66, 0.2);
}

.msg-text {
  font-size: 28rpx;
  color: #f5f5f5;
  line-height: 1.5;
  word-break: break-all;
}

.msg-time {
  font-size: 20rpx;
  color: #6b6b80;
  margin-top: 6rpx;
}

.message-item.is-self .msg-time {
  text-align: right;
}

/* 输入栏 */
.input-bar {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 16rpx 32rpx;
  padding-bottom: calc(16rpx + env(safe-area-inset-bottom));
  background-color: #232338;
  border-top: 1rpx solid #3a3a50;
}

.msg-input {
  flex: 1;
  height: 72rpx;
  background-color: #2a2a3e;
  border-radius: 36rpx;
  padding: 0 28rpx;
  font-size: 28rpx;
  color: #f5f5f5;
}

.input-placeholder {
  color: #6b6b80;
}

.send-btn {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  border-radius: 36rpx;
  padding: 16rpx 32rpx;
}

.send-text {
  font-size: 26rpx;
  color: #1a1a2e;
  font-weight: 600;
}
</style>
