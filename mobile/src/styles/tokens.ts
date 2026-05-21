/**
 * Design Tokens - 掼蛋平台设计令牌
 * 定义所有视觉设计常量，作为设计系统的唯一真相源
 */
export const DesignTokens = {
  colors: {
    primary: '#C41E3A',        // 深红色主色
    primaryDark: '#9B1830',    // 深红色暗色
    primaryLight: '#E8354F',   // 深红色浅色
    gold: '#D4A843',           // 金色强调色
    goldLight: '#F0D68A',      // 金色浅色
    background: '#F5F5F5',     // 页面背景
    surface: '#FFFFFF',        // 卡片/容器背景
    textPrimary: '#1A1A1A',    // 主文字
    textSecondary: '#666666',  // 次要文字
    textTertiary: '#999999',   // 辅助文字
    border: '#EEEEEE',         // 边框
    success: '#52C41A',        // 成功
    warning: '#FAAD14',        // 警告
    error: '#FF4D4F',          // 错误
  },
  spacing: {
    xs: '8rpx',
    sm: '16rpx',
    md: '24rpx',
    lg: '32rpx',
    xl: '48rpx',
  },
  radius: {
    sm: '8rpx',
    md: '16rpx',
    lg: '24rpx',
    xl: '32rpx',
    full: '9999rpx',
  },
  fontSize: {
    xs: '20rpx',
    sm: '24rpx',
    base: '28rpx',
    md: '32rpx',
    lg: '36rpx',
    xl: '40rpx',
    '2xl': '48rpx',
  },
  shadow: {
    sm: '0 2rpx 8rpx rgba(0, 0, 0, 0.04)',
    md: '0 4rpx 16rpx rgba(0, 0, 0, 0.08)',
    lg: '0 8rpx 32rpx rgba(0, 0, 0, 0.12)',
  },
} as const

export type DesignTokensType = typeof DesignTokens
