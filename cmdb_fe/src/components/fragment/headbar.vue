<template>
<div style="display: flex;" :style="{height: windowHeight}">
    <div :style="appBar" style="width: 250px;  height: 100%;" >

        <mu-appbar  style="background-color:#dd4b39">
            <md-avatar>
                <img src='/static/lufei.jpg' alt="People">
            </md-avatar>
            <mu-flat-button label="li hao"/>
        </mu-appbar>
        <CmdbMenu></CmdbMenu>
    </div>
    <div style="flex: 1;">
        <mu-appbar title="测试平台" style="background-color:#dd4b39">
            <mu-icon-button icon="menu" @click="toggle" slot="left"/>
            <mu-icon-button icon="more_vert" slot="right"/>
        </mu-appbar>
        <router-view style="margin:20px 20px 0px 0px"></router-view>
    </div>
</div>
</template>

<script>
import CmdbMenu from '@/components/Cmdb/cmdbmenu'

/* eslint-disable */
export default {
  data () {
    return {
      appBar:{
        marginLeft: '0',
        transition: 'all 0.2s linear'
      },
      windowHeight: 0,
      open: true,
    }
  },
  mounted () {
      this.setHeight()
      window.addEventListener('resize', this.setHeight);
  },
  methods: {
    setHeight () {
        this.windowHeight = window.innerHeight + 'px'
    },
    toggle () {
        this.open = !this.open
        if (this.open === true) {
            this.appBar.marginLeft = '0'
        }
        else{
            this.appBar.marginLeft = '-250px'
        }
    }
  },
    components: {
        CmdbMenu,
    }
}
</script>
<style>
.md-list  {
    padding: 0 0;
}
.md-list-item-content {
    padding: 0 16;
}
</style>
