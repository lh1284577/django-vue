<template>
  <div>
    <mu-list>
            <mu-list-item title="资产管理"  toggleNested>
                <mu-icon slot="left" value="settings" />
                <mu-list-item slot="nested" :title="mem.name" :key="mem.key" v-for="mem in menus" :to="'/Cmdb/' + mem.key" >
                    <mu-icon slot="left" :value="mem.icon"/>
                </mu-list-item>
            </mu-list-item>
    </mu-list>
  </div>
</template>

<script>
/* eslint-disable */
import bus from '@/components/common/bus'

  export default {
    data () {
      return {
        menlist: {
          backgroud: ''
        },
        menus: [{
            name: '机房信息', 
            icon: 'settings',
            key: 'idc'
        }, {
            name: '业务操作',
            icon: 'settings',
            key: 'ops'
        }],
        loading: true
      }
    },
    mounted () {
    },
    created () {
    },
    methods: {
      forname(name) {
        bus.$emit('message', name)
      }
    },
    components: {
    }
  }
</script>