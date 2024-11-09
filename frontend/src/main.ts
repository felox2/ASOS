import './assets/main.css'

import { createPinia } from 'pinia'
import { DataLoaderPlugin } from 'unplugin-vue-router/data-loaders'
import { createApp } from 'vue'

import App from './App.vue'
import { i18n } from './i18n'
import { router } from './router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())

useAuthStore()
  .refresh()
  .then(() => {
    app.use(i18n)
    app.use(DataLoaderPlugin, { router })
    app.use(router)

    app.mount('#app')
  })
