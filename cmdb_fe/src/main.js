// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import MuseUI from 'muse-ui'
import 'muse-ui/dist/muse-ui.css'
import VueMaterial from 'vue-material'
// import 'vue-material/dist/vue-material.min.css'
// import 'vue-material/dist/theme/default.css'
import VueResource from 'vue-resource'
import bus from '@/components/common/bus'
import 'vue-material/dist/vue-material.css'

Vue.use(MuseUI)
Vue.use(VueResource)
Vue.use(VueMaterial)

/* eslint-disable */


Vue.config.productionTip = false
window.NOTIFY_SERVER = process.env.NOTIFY_SERVER

// Vue.http.interceptors.push((request, next) => {
//   if (!request.url.startsWith('http')) {
//     request.url = window.SERVER_ROOT + request.url
//   }
// })

Vue.material.registerTheme('default', {
  primary: 'blue',
  accent: 'red',
  warn: 'red',
  background: 'white'
})

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})


