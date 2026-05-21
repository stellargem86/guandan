<template>
  <view style="min-height: 100vh; background-color: #1a1a2e; padding: 40px;">
    <view style="margin-bottom: 30px;">
      <text style="font-size: 36px; font-weight: 700; color: #f5f5f5; display: block;">掼友圈</text>
      <text style="font-size: 14px; color: #6b6b80; margin-top: 8px; display: block;">同城掼蛋 约局交友</text>
    </view>

    <view style="display: flex; justify-content: space-around; margin-bottom: 30px;">
      <view style="display: flex; flex-direction: column; align-items: center;">
        <view style="width: 50px; height: 50px; background: rgba(246,195,66,0.15); border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(246,195,66,0.2);">
          <text style="font-size: 24px;">📍</text>
        </view>
        <text style="font-size: 12px; color: #b0b0c0; margin-top: 8px;">地图找局</text>
      </view>
      <view style="display: flex; flex-direction: column; align-items: center;">
        <view style="width: 50px; height: 50px; background: rgba(246,195,66,0.15); border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(246,195,66,0.2);">
          <text style="font-size: 24px;">🎯</text>
        </view>
        <text style="font-size: 12px; color: #b0b0c0; margin-top: 8px;">一键组局</text>
      </view>
      <view style="display: flex; flex-direction: column; align-items: center;">
        <view style="width: 50px; height: 50px; background: rgba(246,195,66,0.15); border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(246,195,66,0.2);">
          <text style="font-size: 24px;">🤝</text>
        </view>
        <text style="font-size: 12px; color: #b0b0c0; margin-top: 8px;">商务人脉</text>
      </view>
      <view style="display: flex; flex-direction: column; align-items: center;">
        <view style="width: 50px; height: 50px; background: rgba(246,195,66,0.15); border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(246,195,66,0.2);">
          <text style="font-size: 24px;">🔥</text>
        </view>
        <text style="font-size: 12px; color: #b0b0c0; margin-top: 8px;">热门活动</text>
      </view>
    </view>

    <text style="font-size: 18px; font-weight: 600; color: #f5f5f5; display: block; margin-bottom: 16px;">掼友动态</text>

    <view style="background-color: #2a2a3e; border-radius: 16px; padding: 20px; margin-bottom: 16px;">
      <view style="display: flex; align-items: center; margin-bottom: 12px;">
        <view style="width: 40px; height: 40px; background: linear-gradient(135deg, #f6c342, #d4a537); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
          <text style="font-size: 16px; color: #1a1a2e; font-weight: 700;">张</text>
        </view>
        <view>
          <text style="font-size: 15px; font-weight: 600; color: #f5f5f5; display: block;">张总·金融</text>
          <text style="font-size: 12px; color: #6b6b80; display: block;">10分钟前</text>
        </view>
      </view>
      <text style="font-size: 14px; color: #e0e0e8; line-height: 1.6; display: block;">今晚8点金陵棋牌会所，三缺一，段位A以上优先，结束后聚餐！有意者私信我 🃏</text>
      <view style="display: flex; gap: 20px; margin-top: 12px; padding-top: 12px; border-top: 1px solid #3a3a50;">
        <text style="font-size: 13px; color: #6b6b80;">👍 28</text>
        <text style="font-size: 13px; color: #6b6b80;">💬 12</text>
        <text style="font-size: 13px; color: #6b6b80;">🔄 3</text>
      </view>
    </view>

    <view style="background-color: #2a2a3e; border-radius: 16px; padding: 20px; margin-bottom: 16px;">
      <view style="display: flex; align-items: center; margin-bottom: 12px;">
        <view style="width: 40px; height: 40px; background: linear-gradient(135deg, #f6c342, #d4a537); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
          <text style="font-size: 16px; color: #1a1a2e; font-weight: 700;">李</text>
        </view>
        <view>
          <text style="font-size: 15px; font-weight: 600; color: #f5f5f5; display: block;">李总·科技</text>
          <text style="font-size: 12px; color: #6b6b80; display: block;">30分钟前</text>
        </view>
      </view>
      <text style="font-size: 14px; color: #e0e0e8; line-height: 1.6; display: block;">昨天深掼会月赛夺冠了！连续三局对A打满贯，ELO涨了45分到2780 🏆🎉</text>
      <view style="display: flex; gap: 20px; margin-top: 12px; padding-top: 12px; border-top: 1px solid #3a3a50;">
        <text style="font-size: 13px; color: #6b6b80;">👍 156</text>
        <text style="font-size: 13px; color: #6b6b80;">💬 43</text>
        <text style="font-size: 13px; color: #6b6b80;">🔄 12</text>
      </view>
    </view>

    <view style="background-color: #2a2a3e; border-radius: 16px; padding: 20px; margin-bottom: 16px;">
      <view style="display: flex; align-items: center; margin-bottom: 12px;">
        <view style="width: 40px; height: 40px; background: linear-gradient(135deg, #f6c342, #d4a537); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px;">
          <text style="font-size: 16px; color: #1a1a2e; font-weight: 700;">王</text>
        </view>
        <view>
          <text style="font-size: 15px; font-weight: 600; color: #f5f5f5; display: block;">王姐·教育</text>
          <text style="font-size: 12px; color: #6b6b80; display: block;">2小时前</text>
        </view>
      </view>
      <text style="font-size: 14px; color: #e0e0e8; line-height: 1.6; display: block;">分享一个实战技巧：当手持双王+同花顺时，不要急于出牌，先观察对手出牌节奏。昨晚靠这个策略逆转了两局 ⭐</text>
      <view style="display: flex; gap: 20px; margin-top: 12px; padding-top: 12px; border-top: 1px solid #3a3a50;">
        <text style="font-size: 13px; color: #6b6b80;">👍 89</text>
        <text style="font-size: 13px; color: #6b6b80;">💬 34</text>
        <text style="font-size: 13px; color: #6b6b80;">🔄 21</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
</script>
