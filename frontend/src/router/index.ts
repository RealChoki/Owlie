import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import QuizProf from '../views/QuizProf.vue'
import CreateCourse from '../views/CreateCourse.vue'
import AboutUs from '../views/AboutUs.vue'
import Profile from '../views/Profile.vue'
import courseDashboard from '../views/courseDashboard.vue'

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
      path: '/courses',
      name: 'CreateCourse',
      component: CreateCourse
    },
    {
      path: '/courses/:courseId',
      name: 'courseDashboard',
      component: courseDashboard,
      props: true, // Pass courseId as a prop
    },
    {
      path: '/about',
      name: 'about',
      component: AboutUs,
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
    },
  ],
})

export default router
