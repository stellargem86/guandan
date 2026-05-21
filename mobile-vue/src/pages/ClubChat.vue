<template>
  <div class="page chat-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-back" @click="$router.back()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
        </div>
        <div class="header-center">
          <span class="header-title">金陵掼蛋俱乐部</span>
          <span class="header-members">128人</span>
        </div>
        <div class="header-right">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
        </div>
      </div>
    </div>

    <!-- Chat Messages -->
    <div class="chat-body">
      <!-- System Message -->
      <div class="system-msg">
        <span>--- 今天 ---</span>
      </div>

      <!-- Activity Notice -->
      <div class="notice-card">
        <div class="notice-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#C62828" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        </div>
        <div class="notice-content">
          <h4>活动通知</h4>
          <p>本周六（3月15日）14:00 将举办周末友谊赛，地点：同庆楼3楼。请各位会员准时参加！</p>
        </div>
      </div>

      <!-- Messages -->
      <div v-for="msg in messages" :key="msg.id" class="message" :class="{ 'message-self': msg.isSelf }">
        <div v-if="!msg.isSelf" class="msg-avatar" :style="{ background: msg.avatarColor }">
          {{ msg.author[0] }}
        </div>
        <div class="msg-content">
          <span v-if="!msg.isSelf" class="msg-author">{{ msg.author }}</span>
          <div class="msg-bubble" :class="{ 'bubble-self': msg.isSelf }">
            {{ msg.text }}
          </div>
          <span class="msg-time">{{ msg.time }}</span>
        </div>
        <div v-if="msg.isSelf" class="msg-avatar self-avatar">
          我
        </div>
      </div>

      <!-- Schedule Card -->
      <div class="schedule-card">
        <div class="schedule-header">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#C62828" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          <span>本周赛程安排</span>
        </div>
        <div class="schedule-list">
          <div class="schedule-item">
            <span class="schedule-time">周六 14:00</span>
            <span class="schedule-name">周末友谊赛</span>
          </div>
          <div class="schedule-item">
            <span class="schedule-time">周日 09:00</span>
            <span class="schedule-name">新手训练营</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Bar -->
    <div class="input-bar">
      <div class="input-actions">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>
      </div>
      <input type="text" class="input-field" placeholder="发送消息..." />
      <button class="send-btn">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const messages = [
  {
    id: 1,
    author: '张三丰',
    avatarColor: 'linear-gradient(135deg, #667eea, #764ba2)',
    text: '周六的友谊赛大家都报名了吗？听说这次有新规则',
    time: '10:23',
    isSelf: false
  },
  {
    id: 2,
    author: '李掼王',
    avatarColor: 'linear-gradient(135deg, #4facfe, #00f2fe)',
    text: '我报了！上次的双王规则确实有意思，期待这次的新玩法',
    time: '10:25',
    isSelf: false
  },
  {
    id: 3,
    author: '我',
    avatarColor: '',
    text: '我也报名了，这次能不能分到一组啊哈哈',
    time: '10:28',
    isSelf: true
  },
  {
    id: 4,
    author: '王大炸',
    avatarColor: 'linear-gradient(135deg, #43e97b, #38f9d7)',
    text: '抽签决定配对，上次我和铁柱搭档差点夺冠，这次希望运气好',
    time: '10:30',
    isSelf: false
  },
  {
    id: 5,
    author: '赵铁柱',
    avatarColor: 'linear-gradient(135deg, #fa709a, #fee140)',
    text: '哈哈大炸你太谦虚了，你那一手炸弹简直无敌。对了，这次比赛有奖品吗？',
    time: '10:32',
    isSelf: false
  },
]
</script>

<style scoped>
.chat-page {
  background: #f5f5f5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: var(--gradient-header);
  padding: var(--safe-area-top) var(--spacing-lg) 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  height: var(--header-height);
  display: flex;
  align-items: center;
}

.header-back, .header-right {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-center {
  flex: 1;
  text-align: center;
}

.header-title {
  display: block;
  font-size: 15px;
  font-weight: 600;
  color: white;
}

.header-members {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
}

.chat-body {
  flex: 1;
  padding: 12px var(--spacing-lg);
  padding-bottom: 70px;
  overflow-y: auto;
}

.system-msg {
  text-align: center;
  margin: 12px 0;
}

.system-msg span {
  font-size: 11px;
  color: var(--text-tertiary);
  background: rgba(0, 0, 0, 0.05);
  padding: 3px 10px;
  border-radius: var(--radius-full);
}

.notice-card {
  background: white;
  border-radius: var(--radius-md);
  padding: 12px;
  margin-bottom: 16px;
  display: flex;
  gap: 10px;
  border-left: 3px solid var(--color-primary);
}

.notice-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.notice-content h4 {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.notice-content p {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
}

.message {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.message-self {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}

.self-avatar {
  background: var(--gradient-header);
}

.msg-content {
  max-width: 70%;
}

.msg-author {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-bottom: 3px;
  display: block;
}

.msg-bubble {
  background: white;
  padding: 10px 14px;
  border-radius: 12px 12px 12px 4px;
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-primary);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.bubble-self {
  background: #fff0f0;
  border-radius: 12px 12px 4px 12px;
}

.msg-time {
  font-size: 10px;
  color: var(--text-tertiary);
  margin-top: 3px;
  display: block;
}

.message-self .msg-time {
  text-align: right;
}

.schedule-card {
  background: white;
  border-radius: var(--radius-md);
  padding: 12px;
  margin-top: 8px;
}

.schedule-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.schedule-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.schedule-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 10px;
  background: #fafafa;
  border-radius: var(--radius-sm);
}

.schedule-time {
  font-size: 12px;
  color: var(--color-primary);
  font-weight: 500;
  min-width: 70px;
}

.schedule-name {
  font-size: 13px;
  color: var(--text-primary);
}

.input-bar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px var(--spacing-lg);
  background: white;
  border-top: 1px solid var(--border-lighter);
}

.input-field {
  flex: 1;
  height: 36px;
  background: #f5f5f5;
  border-radius: var(--radius-full);
  padding: 0 14px;
  font-size: 14px;
}

.input-field::placeholder {
  color: var(--text-tertiary);
}

.send-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
