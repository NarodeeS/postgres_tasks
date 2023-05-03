import { createApp } from 'vue'
import App from './App.vue'
import './assets/global.css'
import route from "@/router/index";
import { VueCookieNext } from 'vue-cookie-next'
import { store, key } from './store'



createApp(App).use(VueCookieNext)
        .use(route)
        .use(store, key)
        // .use(VueAnime)
        .mount('#app')

// set default config
VueCookieNext.config({ expire: '7d' })
