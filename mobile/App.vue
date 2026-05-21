<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'

onLaunch(() => {
  console.log('掼蛋平台 App Launch')
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style>
/* 掼蛋平台 - 中国红主题全局样式 */
page {
  background-color: #F5F5F5;
  color: #333333;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  min-height: 100vh;
}

/* 全局滚动条 (H5) */
::-webkit-scrollbar {
  width: 0;
  height: 0;
}

/* uni-app 组件主题覆盖 */
uni-view,
uni-text {
  color: #333333;
}

/* 卡片基础样式 */
.card {
  background-color: #FFFFFF;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.05);
}

/* 红色高亮文字 */
.text-red {
  color: #C41E3A;
}

/* 红色渐变按钮 */
.btn-red {
  background: linear-gradient(135deg, #C41E3A 0%, #E8354A 100%);
  color: #FFFFFF;
  border-radius: 12rpx;
  padding: 20rpx 40rpx;
  font-weight: 600;
  text-align: center;
}

.btn-red:active {
  opacity: 0.85;
  transform: scale(0.98);
}

/* 描边按钮 */
.btn-outline-red {
  border: 1px solid #C41E3A;
  color: #C41E3A;
  border-radius: 12rpx;
  padding: 20rpx 40rpx;
  text-align: center;
  background-color: transparent;
}

/* 分割线 */
.divider {
  height: 1rpx;
  background-color: #EEEEEE;
}
</style>
