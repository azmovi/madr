import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AccountView from '../views/AccountView.vue'
import BookView from '../views/BookView.vue'
import NovelistView from '../views/NovelistView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/conta',
      name: 'conta',
      component: AccountView,
    },
    {
      path: '/livros',
      name: 'livros',
      component: BookView,
    },
    {
      path: '/romancistas',
      name: 'romancistas',
      component: NovelistView,
    },
  ]
})

export default router
