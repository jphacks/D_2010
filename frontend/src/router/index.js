import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/video',
        name: 'video',
        component: () => import('@/views/Video.vue'),
    },
    {
        path: '/video/:videoId',
        component: () => import('@/views/Video.vue'),
        props: true,
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
