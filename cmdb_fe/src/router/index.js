import Vue from 'vue'
import Router from 'vue-router'
import AssetList from '@/components/Cmdb/assetlist'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/Cmdb/:assetType',
      component: AssetList
    }
  ]
})
