import { createApp } from "vue";
import App from "./App.vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import { createRouter, createWebHistory } from "vue-router";
import Home from "./views/Home.vue";
import Login from "./views/Login.vue";
import { setAuthToken } from "./api";

const routes = [
  { path: "/", component: Home, meta: { requiresAuth: true } },
  { path: "/login", component: Login },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Simple navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    setAuthToken(token);
    next();
  }
});

createApp(App).use(ElementPlus).use(router).mount("#app");
