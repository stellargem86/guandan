import './pages-json-js'
import './src/styles/global.scss'
// @ts-ignore
import { plugin as __plugin } from '@dcloudio/uni-h5'
import { createSSRApp as createVueApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

console.log('main.ts loaded - manual bootstrap')

export function createApp() {
  const app = createVueApp(App)
  const pinia = createPinia()
  app.use(pinia)
  return { app }
}

createApp().app.use(__plugin).mount('#app')
