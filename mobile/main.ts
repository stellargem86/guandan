import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

console.log('main.ts loaded!')

export function createApp() {
  console.log('createApp called!')
  const app = createSSRApp(App)
  const pinia = createPinia()
  app.use(pinia)
  return { app }
}
