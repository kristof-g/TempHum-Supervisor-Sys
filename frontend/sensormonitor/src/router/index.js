import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/components/Login'
import ConnectedNodes from '@/components/ConnectedNodes'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/stations',
      name: 'ConnectedNodes',
      component: ConnectedNodes
    }
  ]
})
