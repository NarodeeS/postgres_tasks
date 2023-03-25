

import { createRouter, createWebHistory } from 'vue-router'
import AccauntPage from "@/views/AccountPage.vue";
import LoginPage from "@/views/LoginPage.vue"
import MainPage from "@/views/MainPage.vue"

const routes = [
  {
    path: "/",
    name: "mainPage",
    component: MainPage
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage
  },
  {
    path: "/account",
    name: "account",
    component: AccauntPage
  },

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router