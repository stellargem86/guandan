/**
 * 支付相关组合函数
 */
import { ref } from 'vue'

interface PaymentParams {
  timeStamp: string
  nonceStr: string
  package: string
  signType: string
  paySign: string
}

export function usePayment() {
  const paying = ref(false)
  const payError = ref<string | null>(null)

  /** 调起微信支付 */
  async function requestPayment(params: PaymentParams): Promise<boolean> {
    paying.value = true
    payError.value = null

    return new Promise((resolve) => {
      uni.requestPayment({
        provider: 'wxpay',
        ...params,
        success: () => {
          resolve(true)
        },
        fail: (err) => {
          payError.value = err.errMsg || '支付失败'
          resolve(false)
        },
        complete: () => {
          paying.value = false
        },
      })
    })
  }

  return {
    paying,
    payError,
    requestPayment,
  }
}
