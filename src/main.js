import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'

import { routes } from './routes';

Vue.use(VueRouter);

Vue.prototype.$serverUrl = "http://127.0.0.1:7777/"

Vue.filter('readable', timestamp => {
  var date = new Date(timestamp * 1000);

  var year = date.getFullYear();
  var month = date.getMonth();
  var day = date.getDay();
  var hours = date.getHours();
  var minutes = "0" + date.getMinutes();
  var seconds = "0" + date.getSeconds();

  var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

  return day + ". " + month + ". " + year + " " + formattedTime;
})

Vue.filter('size', size => {
  return size / 1000 + " KB";
})

const router = new VueRouter({
  mode: 'history',
  routes
})


new Vue({
  el: '#app',
  router,
  render: h => h(App),
})
