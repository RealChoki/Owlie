import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
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
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
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
