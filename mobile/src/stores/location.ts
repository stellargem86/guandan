/**
 * 位置状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLocationStore = defineStore('location', () => {
  const latitude = ref<number>(0)
  const longitude = ref<number>(0)
  const city = ref<string>('')
  const hasPermission = ref<boolean>(false)

  function setLocation(lat: number, lng: number) {
    latitude.value = lat
    longitude.value = lng
  }

  function setCity(name: string) {
    city.value = name
  }

  function setPermission(granted: boolean) {
    hasPermission.value = granted
  }

  return {
    latitude,
    longitude,
    city,
    hasPermission,
    setLocation,
    setCity,
    setPermission,
  }
})
