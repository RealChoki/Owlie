import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import QuizProf from '../views/QuizProf.vue'
import CreateCourseAssistant from '../views/CreateCourseAssistant.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/quiz',
      name: 'quiz',
      component: () => QuizProf,
    },
    {
      path: '/create-assistant',
      name: 'CreateCourseAssistant',
      component: CreateCourseAssistant
    }
  ],
})

export default router
