import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'
// @ts-ignore
import { plugin } from '@dcloudio/uni-h5'
import './pages.json.js'
import App from './App.vue'

console.log('main.ts loaded - manual bootstrap')

function createApp() {
  const app = createSSRApp(App)
  const pinia = createPinia()
  app.use(pinia)
  return { app }
}

const { app } = createApp()
app.use(plugin).mount('#app')
