<template>
  <div>
      <component :is="assetListType[$route.params.assetType]" ></component>
  </div>
</template>

<script>
/* eslint-disable */

  import idclist from './asset/idclist'
  import opslist from './asset/opslist'
  export default {
    data () {
      return {
        assetListType: {
          'idc': 'idclist',
          'ops': 'opslist'
        },
        loading: true
      }
    },
    mounted () {
    },
    created () {
    },
    methods: {
    },
    components: {
      idclist,
      opslist
    }
  }
</script>