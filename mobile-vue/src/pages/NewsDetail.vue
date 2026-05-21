<template>
  <div class="page news-detail-page">
    <!-- Header -->
    <div class="header">
      <div class="header-content">
        <div class="header-back" @click="$router.back()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round"><polyline points="15 18 9 12 15 6"/></svg>
        </div>
        <div class="header-title">文章详情</div>
        <div class="header-right">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
        </div>
      </div>
    </div>

    <!-- Article Content -->
    <div class="article-content">
      <h1 class="article-title">掼蛋从0到1：新手入门完全教学指南</h1>
      
      <div class="article-author">
        <div class="author-avatar">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        </div>
        <div class="author-info">
          <span class="author-name">掼蛋学院</span>
          <span class="author-date">2024-03-10 · 3.2万阅读</span>
        </div>
        <button class="follow-btn">关注</button>
      </div>

      <!-- Content Body -->
      <div class="content-body">
        <h2>一、什么是掼蛋？</h2>
        <p>
          掼蛋是一种在江苏、安徽等地区广泛流行的扑克牌游戏，又名"炒地皮"。该游戏起源于江苏淮安，由当地的"跑得快"和"八十分"融合发展而来，兼具竞技性和趣味性。
        </p>
        <p>
          掼蛋使用两副标准扑克牌（含大小王共108张），由四人参与，分为两两对抗的两组进行比赛。
        </p>

        <!-- Image Placeholder -->
        <div class="content-image">
          <div class="image-placeholder">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            <span>掼蛋牌型示例图</span>
          </div>
        </div>

        <h2>二、基本牌型介绍</h2>
        <p>
          掼蛋的牌型丰富多样，从小到大依次为：单张、对子、三条、三带二、顺子（5张及以上）、同花顺、炸弹（4张及以上同点数）、火箭（大小王）。
        </p>
        <p>
          其中，炸弹的大小按张数和点数排列。四张炸弹 < 五张炸弹 < 六张炸弹，以此类推。同张数的炸弹按点数大小比较。
        </p>

        <h2>三、进贡与抗贡</h2>
        <p>
          掼蛋中有独特的"进贡"机制。上一局的输家需要在下一局开始时，将手中最大的一张牌进贡给上一局的赢家。如果输家手中有两个大王，则可以"抗贡"，即不需要进贡。
        </p>

        <!-- Image Placeholder -->
        <div class="content-image">
          <div class="image-placeholder alt">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
            <span>进贡规则说明</span>
          </div>
        </div>

        <h2>四、配合与策略</h2>
        <p>
          掼蛋是一个团队合作的游戏，与搭档的配合至关重要。好的配合能够让你们在牌力不占优势的情况下也能取得胜利。
        </p>
        <p>
          常见的配合策略包括：主动叫牌让搭档了解你的牌力、合理安排出牌顺序为搭档创造机会、以及在关键时刻用炸弹为搭档保驾护航。
        </p>
      </div>
    </div>

    <!-- Bottom Action Bar -->
    <div class="bottom-bar">
      <div class="bar-input">
        <input type="text" placeholder="写评论..." readonly />
      </div>
      <div class="bar-actions">
        <div class="bar-action">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="1.8"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          <span>326</span>
        </div>
        <div class="bar-action">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          <span>48</span>
        </div>
        <div class="bar-action">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="1.8"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
          <span>分享</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.news-detail-page {
  background: var(--bg-card);
  min-height: 100vh;
  padding-bottom: 60px;
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

.header-title {
  flex: 1;
  text-align: center;
  font-size: 17px;
  font-weight: 600;
  color: var(--text-white);
}

.article-content {
  padding: var(--spacing-xl);
}

.article-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
  margin-bottom: 16px;
}

.article-author {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-lighter);
}

.author-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--gradient-header);
  display: flex;
  align-items: center;
  justify-content: center;
}

.author-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.author-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.author-date {
  font-size: 11px;
  color: var(--text-tertiary);
}

.follow-btn {
  padding: 5px 14px;
  background: var(--color-primary);
  color: white;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
}

.content-body h2 {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 24px 0 12px;
  padding-left: 10px;
  border-left: 3px solid var(--color-primary);
}

.content-body p {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-secondary);
  margin-bottom: 12px;
  text-align: justify;
}

.content-image {
  margin: 20px 0;
}

.image-placeholder {
  height: 180px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.image-placeholder.alt {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.image-placeholder span {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px var(--spacing-lg);
  background: var(--bg-card);
  border-top: 1px solid var(--border-light);
}

.bar-input {
  flex: 1;
}

.bar-input input {
  width: 100%;
  height: 32px;
  background: #f5f5f5;
  border-radius: var(--radius-full);
  padding: 0 14px;
  font-size: 13px;
}

.bar-input input::placeholder {
  color: var(--text-tertiary);
}

.bar-actions {
  display: flex;
  gap: 16px;
}

.bar-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.bar-action span {
  font-size: 10px;
  color: var(--text-tertiary);
}
</style>
