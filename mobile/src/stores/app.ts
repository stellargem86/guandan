/**
 * 应用全局状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const loading = ref(false)
  const networkConnected = ref(true)
  const systemInfo = ref<UniApp.GetSystemInfoResult | null>(null)

  function setLoading(value: boolean) {
    loading.value = value
  }

  function setNetworkStatus(connected: boolean) {
    networkConnected.value = connected
  }

  function setSystemInfo(info: UniApp.GetSystemInfoResult) {
    systemInfo.value = info
  }

  return {
    loading,
    networkConnected,
    systemInfo,
    setLoading,
    setNetworkStatus,
    setSystemInfo,
  }
})
