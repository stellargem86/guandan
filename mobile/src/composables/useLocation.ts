/**
 * 地理位置相关组合函数
 */
import { ref } from 'vue'

interface LocationInfo {
  latitude: number
  longitude: number
}

export function useLocation() {
  const location = ref<LocationInfo | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  /** 获取当前位置 */
  async function getCurrentLocation(): Promise<LocationInfo | null> {
    loading.value = true
    error.value = null

    return new Promise((resolve) => {
      uni.getLocation({
        type: 'gcj02',
        success: (res) => {
          location.value = {
            latitude: res.latitude,
            longitude: res.longitude,
          }
          resolve(location.value)
        },
        fail: (err) => {
          error.value = err.errMsg || '获取位置失败'
          resolve(null)
        },
        complete: () => {
          loading.value = false
        },
      })
    })
  }

  return {
    location,
    loading,
    error,
    getCurrentLocation,
  }
}
