<template>
  <view class="payment-btn-wrapper">
    <button
      class="payment-btn btn-gold"
      :disabled="disabled || loading"
      @click="handlePay"
    >
      <text v-if="loading" class="btn-loading">支付中...</text>
      <text v-else class="btn-text">
        {{ buttonText || `¥${price} 立即支付` }}
      </text>
    </button>
    <text v-if="originalPrice" class="original-price">原价 ¥{{ originalPrice }}</text>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface PaymentButtonProps {
  price: number | string
  originalPrice?: number | string
  buttonText?: string
  disabled?: boolean
}

defineProps<PaymentButtonProps>()
const emit = defineEmits(['pay'])

const loading = ref(false)

const handlePay = () => {
  if (loading.value) return
  loading.value = true
  emit('pay')
  // Parent is responsible for resetting loading state
  setTimeout(() => {
    loading.value = false
  }, 3000)
}
</script>

<style scoped>
.payment-btn-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
}

.payment-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 88rpx;
  border: none;
  outline: none;
}

.payment-btn[disabled] {
  opacity: 0.5;
}

.btn-text {
  font-size: 32rpx;
  font-weight: 700;
  color: #1a1a2e;
}

.btn-loading {
  font-size: 28rpx;
  color: #1a1a2e;
}

.original-price {
  font-size: 24rpx;
  color: #6b6b80;
  text-decoration: line-through;
}
</style>
