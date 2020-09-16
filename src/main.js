import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'

import { routes } from './routes';

Vue.use(VueRouter);

Vue.prototype.$serverUrl = "http://127.0.0.1:7777/"

const router = new VueRouter({
  mode: 'history',
  routes
})


new Vue({
  el: '#app',
  router,
  render: h => h(App),
})
