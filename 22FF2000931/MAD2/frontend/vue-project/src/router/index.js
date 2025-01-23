import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginForm from '../views/Login.vue'
import Udash from '../views/Udash.vue'
import SignupForm from '../views/Signup.vue'
import liblogin from '../views/Liblogin.vue'
import Adash from '../views/Adash.vue'
import Addsection from '../views/Addsection.vue'
import Sdetails from '../views/Sdetails.vue'
import Addbooks from '../views/Addbooks.vue'
import Book from '../views/Book.vue'
import Abook from '../views/Abook.vue'
import Editsection from '../views/Editsection.vue'
import Editbook from '../views/Editbook.vue'
import Profile from '../views/Profile.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginForm
    },
    {
      path: '/',
      name: 'Home',
      component: HomeView

    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path : '/udash',
      name: "udash",
      component : Udash
    },
    {
      path : '/signup',
      name: "signup",
      component:SignupForm
    },
    {
      path : '/liblogin',
      name: "liblogin",
      component : liblogin
    },
    {
      path : '/adash',
      name: "adash",
      component : Adash
    },
    {
      path : '/addsection',
      name: "addsection",
      component : Addsection
    },
    {
      path : '/sdetails/:id',
      name: "sdetails",
      component : Sdetails,
    },
    {
      path : '/addbooks/:sid',
      name: "addbooks",
      component : Addbooks,
    },
    {
      path : '/book/:bid',
      name: "book",
      component : Book,
      // props:true
    },
    {
      path : '/abook/:bid',
      name: "abook",
      component : Abook,
      // props:true
    },
    {
      path : '/editsection/:sid',
      name: "editsection",
      component : Editsection,
      // props:true
    },
    {
      path : '/editbook/:bid',
      name: "editbook",
      component : Editbook,
      // props:true
    },
    {
      path : '/userprofile',
      name: "userprofile",
      component : Profile,
      // props:true
    }
  ]
})
 
export default router
