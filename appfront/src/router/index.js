import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Home from '@/components/Home'
import Test from '@/components/Test'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/test',
      name: 'test',
      component: Test
    },
    {
      path: '/hello',
      name: 'hello',
      component: HelloWorld
    }
  ]
})
