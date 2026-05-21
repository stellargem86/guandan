<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AdminLayout from '@/layouts/AdminLayout.vue'
import MerchantLayout from '@/layouts/MerchantLayout.vue'
import OrganizerLayout from '@/layouts/OrganizerLayout.vue'

const route = useRoute()

const layout = computed(() => {
  const portal = route.meta.portal as string | undefined
  if (portal === 'merchant') return MerchantLayout
  if (portal === 'organizer') return OrganizerLayout
  if (portal === 'admin') return AdminLayout
  return null
})
</script>

<template>
  <component :is="layout" v-if="layout">
    <router-view />
  </component>
  <router-view v-else />
</template>
