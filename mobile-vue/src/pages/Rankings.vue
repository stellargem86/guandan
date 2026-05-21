<template>
  <div class="page rankings-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-title">天梯榜</div>
      </div>
    </div>

    <!-- Toggle Tabs -->
    <div class="toggle-tabs">
      <div class="toggle-bg" :class="{ right: activeType === 'club' }"></div>
      <div class="toggle-item" :class="{ active: activeType === 'personal' }" @click="activeType = 'personal'">个人榜</div>
      <div class="toggle-item" :class="{ active: activeType === 'club' }" @click="activeType = 'club'">俱乐部榜</div>
    </div>

    <!-- Category Pills -->
    <div class="category-pills">
      <div
        v-for="cat in categories"
        :key="cat"
        class="category-pill"
        :class="{ active: activeCat === cat }"
        @click="activeCat = cat"
      >{{ cat }}</div>
    </div>

    <!-- Top 3 Podium -->
    <div class="podium">
      <div class="podium-decorations">
        <span class="suit suit-spade">♠</span>
        <span class="suit suit-heart">♥</span>
        <span class="suit suit-diamond">♦</span>
        <span class="suit suit-club">♣</span>
      </div>
      <div class="podium-row">
        <!-- 2nd Place -->
        <div class="podium-item second">
          <div class="podium-rank">2</div>
          <div class="podium-avatar silver">
            <span>李</span>
          </div>
          <div class="podium-name">李掼王</div>
          <div class="podium-score">ELO 2580</div>
        </div>
        <!-- 1st Place -->
        <div class="podium-item first">
          <div class="podium-crown">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#FFD700"><path d="M5 16L3 5l5.5 5L12 4l3.5 6L21 5l-2 11H5z"/><path d="M5 19h14v2H5z"/></svg>
          </div>
          <div class="podium-avatar gold">
            <span>张</span>
          </div>
          <div class="podium-name">张三丰</div>
          <div class="podium-score">ELO 2680</div>
        </div>
        <!-- 3rd Place -->
        <div class="podium-item third">
          <div class="podium-rank">3</div>
          <div class="podium-avatar bronze">
            <span>王</span>
          </div>
          <div class="podium-name">王大炸</div>
          <div class="podium-score">ELO 2520</div>
        </div>
      </div>
    </div>

    <!-- Ranking List -->
    <div class="rank-list">
      <div v-for="player in rankList" :key="player.rank" class="rank-item">
        <span class="rank-num">{{ player.rank }}</span>
        <div class="rank-avatar" :style="{ background: player.color }">
          <span>{{ player.name[0] }}</span>
        </div>
        <div class="rank-info">
          <span class="rank-name">{{ player.name }}</span>
          <span class="rank-club">{{ player.club }}</span>
        </div>
        <div class="rank-elo">
          <span class="elo-value">{{ player.elo }}</span>
          <span class="elo-change" :class="player.change > 0 ? 'up' : 'down'">
            {{ player.change > 0 ? '+' : '' }}{{ player.change }}
          </span>
        </div>
      </div>
    </div>

    <!-- Bottom spacer -->
    <div class="bottom-spacer"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeType = ref('personal')
const activeCat = ref('全部')
const categories = ['全部', '初级', '中级', '高级', '大师']

const rankList = [
  { rank: 4, name: '赵铁柱', club: '金陵掼蛋俱乐部', elo: 2480, change: 15, color: 'linear-gradient(135deg, #667eea, #764ba2)' },
  { rank: 5, name: '孙悟空', club: '南京掼蛋精英会', elo: 2450, change: -8, color: 'linear-gradient(135deg, #f093fb, #f5576c)' },
  { rank: 6, name: '周伯通', club: '鼓楼掼蛋社', elo: 2420, change: 22, color: 'linear-gradient(135deg, #4facfe, #00f2fe)' },
  { rank: 7, name: '钱多多', club: '秦淮棋牌会', elo: 2390, change: -3, color: 'linear-gradient(135deg, #43e97b, #38f9d7)' },
  { rank: 8, name: '吴用兵', club: '玄武掼蛋联盟', elo: 2370, change: 10, color: 'linear-gradient(135deg, #fa709a, #fee140)' },
  { rank: 9, name: '郑大帅', club: '江宁掼蛋协会', elo: 2350, change: 5, color: 'linear-gradient(135deg, #a18cd1, #fbc2eb)' },
  { rank: 10, name: '冯天王', club: '建邺精英社', elo: 2330, change: -12, color: 'linear-gradient(135deg, #ffecd2, #fcb69f)' },
]
</script>

<style scoped>
.rankings-page {
  background: var(--bg-page);
  min-height: 100vh;
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
  justify-content: center;
}

.header-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-white);
}

.toggle-tabs {
  display: flex;
  margin: 12px var(--spacing-lg);
  background: var(--bg-card);
  border-radius: var(--radius-full);
  padding: 3px;
  position: relative;
  box-shadow: var(--shadow-card);
}

.toggle-bg {
  position: absolute;
  top: 3px;
  left: 3px;
  width: calc(50% - 3px);
  height: calc(100% - 6px);
  background: var(--color-primary);
  border-radius: var(--radius-full);
  transition: transform 0.3s ease;
}

.toggle-bg.right {
  transform: translateX(100%);
}

.toggle-item {
  flex: 1;
  text-align: center;
  padding: 8px 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  position: relative;
  z-index: 1;
  transition: color 0.3s;
}

.toggle-item.active {
  color: white;
}

.category-pills {
  display: flex;
  gap: 8px;
  padding: 0 var(--spacing-lg) 12px;
  overflow-x: auto;
}

.category-pill {
  flex-shrink: 0;
  padding: 5px 14px;
  border-radius: var(--radius-full);
  font-size: 12px;
  color: var(--text-secondary);
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  transition: all 0.2s;
}

.category-pill.active {
  background: #fff0f0;
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.podium {
  background: var(--bg-card);
  margin: 0 var(--spacing-lg);
  border-radius: var(--radius-md);
  padding: 24px 16px 20px;
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
}

.podium-decorations {
  position: absolute;
  top: 8px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  opacity: 0.08;
  font-size: 40px;
}

.suit-heart, .suit-diamond {
  color: var(--color-primary);
}

.podium-row {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 16px;
}

.podium-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.podium-item.first {
  margin-bottom: 20px;
}

.podium-crown {
  margin-bottom: -4px;
}

.podium-rank {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
  color: var(--text-secondary);
}

.podium-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  font-weight: 700;
}

.podium-item.first .podium-avatar {
  width: 68px;
  height: 68px;
  font-size: 22px;
}

.podium-avatar.gold {
  background: linear-gradient(135deg, #FFD700, #FFA000);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.4);
}

.podium-avatar.silver {
  background: linear-gradient(135deg, #B0BEC5, #78909C);
  box-shadow: 0 4px 12px rgba(120, 144, 156, 0.3);
}

.podium-avatar.bronze {
  background: linear-gradient(135deg, #FFAB91, #D84315);
  box-shadow: 0 4px 12px rgba(216, 67, 21, 0.3);
}

.podium-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.podium-score {
  font-size: 11px;
  color: var(--text-price);
  font-weight: 600;
}

.rank-list {
  margin: 12px var(--spacing-lg) 0;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.rank-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-lighter);
}

.rank-item:last-child {
  border-bottom: none;
}

.rank-num {
  width: 24px;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-tertiary);
  text-align: center;
}

.rank-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.rank-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.rank-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.rank-club {
  font-size: 11px;
  color: var(--text-tertiary);
}

.rank-elo {
  text-align: right;
}

.elo-value {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  display: block;
}

.elo-change {
  font-size: 11px;
  font-weight: 500;
}

.elo-change.up {
  color: var(--color-success);
}

.elo-change.down {
  color: var(--color-danger);
}

.bottom-spacer {
  height: calc(var(--tabbar-height) + 20px);
}
</style>
