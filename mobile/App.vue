<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('深掼会 App Launch')
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* 深掼会 - 全局深色奢华主题样式 */
page {
  background-color: #1a1a2e;
  color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  min-height: 100vh;
}

/* 全局滚动条 (H5) */
::-webkit-scrollbar {
  width: 0;
  height: 0;
}

/* uni-app 组件深色主题覆盖 */
uni-view,
uni-text {
  color: #f5f5f5;
}

/* 卡片基础样式 */
.card {
  background-color: #2a2a3e;
  border-radius: 24rpx;
  padding: 24rpx;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

/* 金色高亮文字 */
.text-gold {
  color: #f6c342;
}

/* 金色渐变按钮 */
.btn-gold {
  background: linear-gradient(135deg, #f6c342 0%, #d4a537 100%);
  color: #1a1a2e;
  border-radius: 16rpx;
  padding: 20rpx 40rpx;
  font-weight: 600;
  text-align: center;
}

.btn-gold:active {
  opacity: 0.85;
  transform: scale(0.98);
}

/* 描边按钮 */
.btn-outline-gold {
  border: 1px solid rgba(246, 195, 66, 0.5);
  color: #f6c342;
  border-radius: 16rpx;
  padding: 20rpx 40rpx;
  text-align: center;
  background-color: transparent;
}

/* 分割线 */
.divider {
  height: 1rpx;
  background-color: #3a3a50;
}
</style>
