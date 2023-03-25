import { createApp } from 'vue'
import App from './App.vue'
import './assets/global.css'
import route from "@/router/index";
import { VueCookieNext } from 'vue-cookie-next'

createApp(App).use(VueCookieNext).use(route).mount('#app')

// set default config
VueCookieNext.config({ expire: '7d' })
