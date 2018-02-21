<template>
  <div id="app">
      <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700,400italic|Material+Icons">
    <headbar ref="headbar"></headbar>
  </div>
</template>

<script>
/* eslint-disable */
import headbar from '@/components/fragment/headbar'
import bus from '@/components/common/bus'

export default {
  name: 'App',
  data () {
      return {
      }
  },
  computed: {
  },
  created () {
  },
  components: {
    headbar,
  },
  watch: {
  },
  methods: {
  }
}
</script>
