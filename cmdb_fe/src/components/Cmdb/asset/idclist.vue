<template>
    <div>
        <md-table-card>
            <md-toolbar v-if="selected.length === 0" style="background:#2196f3" >
                <h1 class="md-title" style="color:white" >机房信息</h1>
                <md-button class="md-icon-button">
                <md-icon @click.native="opendefmenu">add</md-icon>
                </md-button>

                <md-button class="md-icon-button">
                <md-icon>search</md-icon>
                </md-button>

                    <!-- 搜索 -->
                <form v-if="selected.length === 0" novalidate @submit.stop.prevent="submit">
                <md-input-container md-inline>
                    <md-input v-model="search" @input="searchOnTable"></md-input>
                </md-input-container>
                </form>
            </md-toolbar>

                <!-- 删除烂 -->
                <md-button  v-else class="md-primary md-raised" style="background:#dd4b39" @click.native="opendelete">{{ getAlternateLabel(selected) }}</md-button>

        <!-- 搜索为空，提示信息 -->
            <div v-if="searched.length === 0 " style="text-align: center;">
                <img :src="`/static/nothing.jpg`" style="margin: 2em; height: 10em"/>
                <div style="padding: 1em;color:#dd4b39"><md-icon>info</md-icon> 没有东西</div>
                </div>

            <md-table v-else md-sort="dessert" md-sort-type="desc" @select="onSelect">
                <md-table-header>
                <md-table-row>
                    <md-table-head >主机名</md-table-head>
                    <md-table-head >IP</md-table-head>
                    <md-table-head >环境</md-table-head>
                    <md-table-head>操作</md-table-head>
                </md-table-row>
                </md-table-header>

                <!-- 表单 -->
                <md-table-body>
                <md-table-row v-for="(row, rowIndex) in searched" :key="rowIndex" :md-item="row"  md-selection >
                    <md-table-cell>
                    {{ row.name}}
                    </md-table-cell>
                    <md-table-cell>
                    {{ row.ip}}
                    </md-table-cell>
                    <md-table-cell>
                    {{ row.env}}
                    </md-table-cell>
                    <md-table-cell @click.stop @click.native="configmenu(row)" >
                        <md-button class="md-icon-button">
                            <md-icon>edit</md-icon>
                        </md-button>
                    </md-table-cell>
                </md-table-row>
                </md-table-body>
            </md-table>
        </md-table-card>

        <!-- 新建框 -->
        <md-dialog :md-active.sync="showDialog" style="width:1000px;hegih:800px" >
                <p>
                    <mu-dialog :open="showDialog" @close="showDialog = false" title="添加服务器" scrollable >
                        <mu-menu>
                            <mu-text-field style="font-size:18px" label="名称" v-model="defmenu.name"  fullWidth/>
                            <mu-text-field style="font-size:18px" label="IP" v-model="defmenu.ip"  fullWidth/>
                            <mu-text-field style="font-size:18px" label="环境" v-model="defmenu.env"  fullWidth/>
                        </mu-menu>
                        <mu-flat-button secondary label="确定" @click="add(defmenu)" slot="actions"/>
                        <mu-flat-button  label="关闭" @click="showDialog = false" slot="actions"/>
                    </mu-dialog>
                </p>
        </md-dialog>

        <!-- 编辑框 -->
        <md-dialog :md-active.sync="showDialog1" style="width:1000px;hegih:800px" >
                <p>
                    <mu-dialog :open="showDialog1" @close="showDialog1 = false" title="添加服务器" scrollable >
                        <mu-menu>
                            <mu-text-field style="font-size:18px" label="名称" v-model="defmenu.name"  fullWidth/>
                            <mu-text-field style="font-size:18px" label="IP" v-model="defmenu.ip"  fullWidth/>
                            <mu-text-field style="font-size:18px" label="环境" v-model="defmenu.env"  fullWidth/>
                        </mu-menu>
                        <mu-flat-button secondary label="确定" @click="config(defmenu)" slot="actions"/>
                        <mu-flat-button  label="关闭" @click="showDialog1 = false" slot="actions"/>
                    </mu-dialog>
                </p>
        </md-dialog>

            <!-- 删除确认框 -->
        <mu-dialog :open="deldialog" title="确定删除">
            <mu-flat-button slot="actions" primary @click.native="remove(selected)" label="确定"/>
            <mu-flat-button slot="actions" @click="closedelete" primary label="取消"/>
        </mu-dialog>
    </div>
</template>

<script>
/* eslint-disable */
  const toLower = text => {
    return text.toString().toLowerCase()
  }

  const searchByName = (items, term) => {
    if (term) {
      return items.filter(item => toLower(JSON.stringify(item)).includes(toLower(term)))
    }

    return items
  }
export default {

    data: () => ({
        showDialog: false,
        showDialog1: false,
        search: null,
        searched: [],
        selected: [],
        open: false,
        trigger: null,
        deldialog: false,   
        defmenu: {
            name: '',
            ip: '',
            env: ''
        },
        menus: [
        {
            name: '李浩',
            ip: '127.0.0.1',
            env: 'prod',

        },
        {
            name: '李浩',
            ip: '192.168.1.1',
            env: 'test',

        }
        ]
    }),
    mounted () {
        this.loadidclist()
    },
    methods: {
        opendelete () {
            this.deldialog = true
        }, 
        closedelete () {
            this.deldialog = false
        }, 
        searchOnTable (item) {
            this.searched = searchByName(this.menus, item)
        },
        onSelect (items) {
            this.$emit('selectform',items)
            this.selected = items
        },
        getAlternateLabel (count) {
            return `所需要删除项目 ${count.length}个`
        },
        configmenu (item) {
            Object.assign(this.defmenu,item)
            this.showDialog1 = true
        },
        opendefmenu () {
            this.defmenu =  {
                name: '',
                ip: '',
                env: ''
            }
            this.showDialog = true
        },

        add (item) {
            var form = JSON.parse(JSON.stringify(item))
            this.$http.post('http://test.com/yunwei/api/AESSLIST/',form).then(response => {
            if (response.data.ok != false) {
                this.selected = []
                this.searched.push(form)
                this.showDialog = false
            } else {
                alert('创建 IDC 出错: ' + response.data.message)
            }
            })
        },
        watch: {
            defmenu: {
                deep: true,
                    handler (val) {
                }
            }
        },
        remove (obj) {
            let ids = obj.map(item => item)
            obj.map(item => 
                this.$http.delete('http://test.com/yunwei/api/AESSLIST/' + item.id + '/').then(response => {
                    if (response.data.ok != false) {
                        this.searched = this.searched.filter(item => !ids.includes(item))
                        this.selected = []
                        this.deldialog = false
                    }
                })
            )
        },
        config (obj) {
            var form = JSON.parse(JSON.stringify(obj))
            this.$http.put('http://test.com/yunwei/api/AESSLIST/'+ obj.id + '/',form).then(response => {
            if (response.data.ok != false) {
                this.selected = []
                this.searched = this.searched.filter(item => ![obj.id].includes(item.id))
                this.searched.push(form)
                this.showDialog1 = false
            } else {
                alert('创建 IDC 出错: ' + response.data.message)
            }
            })
        },
        loadidclist () {
            // 获取表数据
            this.$http.get('http://test.com/yunwei/api/AESSLIST/').then(response => {
                if (response.data.ok != false) {
                    this.menus = response.data
                    this.searched = this.menus
                }
            })
            // this.searched = this.menus
        }
    }
}
</script>


<style>
</style>
