<template>
  <div class="phone-viewport">
      <form   style="margin:50px 50px 0px 0px">

        <mu-flexbox >
            <mu-flexbox-item align="center">
                <h2 >任务管理</h2>
            </mu-flexbox-item>
        </mu-flexbox>
      <md-whiteframe md-elevation="1">

        <mu-flexbox style="margin:40px 40px 0px 0px">
            <mu-flexbox-item >
                <div>
                    <table class="infoTable" style="text-align:right;margin:40px 40px 40px 40px;float:left;">
                        <tbody>
                        <tr>
                            <th>脚本来源:</th>
                            <td style="width:300px">
                                <md-input-container>
                                    <md-input v-model="deploylist.resource"></md-input>
                                </md-input-container>
                            </td>
                        </tr>
                        <tr>
                            <th>执行用户:</th>
                            <td>
                                <md-input-container >
                                    <md-input v-model="deploylist.user"></md-input>
                                </md-input-container>
                            </td>
                        </tr>
                        <tr>
                            <th>目标服务器:</th>
                            <td>
                                <div style="float:left">
                                    <div>
                                        <md-button class="md-primary md-raised" id="custom" @click.native="openDialog('dialog1')">选择服务器</md-button>
                                    </div>
                                        <a>(ansible无需选择服务器)</a>
                                        <div class="phone-viewport">
                                            <md-list v-for="(item,index) in selectip" :key="index">
                                                <md-list-item>{{item}}</md-list-item>
                                            </md-list>
                                        </div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <th>脚本参数:</th>
                            <td>
                                <md-input-container>
                                    <md-textarea v-model="deploylist.args"></md-textarea>
                                </md-input-container>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
                <div>
                    <md-whiteframe md-elevation="1" style="float:right;margin:40px 200px 100px 0px;width:600px; height:300px;">
                        <md-whiteframe md-elevation="1">
                            <mu-linear-progress v-show="deployLoading" :size="5" color="red" />
                            <md-card-actions style="justify-content: flex-start">
                                <md-button class="md-dense" style="padding: .2em .6em">
                                    <md-icon :style="outstatus">error</md-icon>
                                    {{outstatus.des}}
                                </md-button>
                            </md-card-actions>

                            <md-card-content style="padding: 0; height: 20em; overflow-y: auto; background: #333; color: #FFF; padding: .5em" id="deploylog">
                            <md-tooltip>点击放大日志</md-tooltip>
                                <pre v-if="fristactive">



            此程序为测试平台，仅支持: ansible / bash / python
            由于测试原因，请连接服务器打通ssh
            默认所有脚本都会放置在目标地址/tmp目录下进行远程执行
            bash / python 并发会导致数据返回结果混乱，建议使用 ansible
                                </pre>
                                <pre v-else>
    {{output}}  
                                </pre>
                            </md-card-content>
                            <md-card-actions style="justify-content: flex-start">
                                <md-button class="md-dense" @click.native="deploy()" style="padding: .2em .6em">
                                    <md-icon style="font-size: 1.4em">build</md-icon>
                                    {{outstatus.ops}}
                                </md-button>
                            </md-card-actions>
                        </md-whiteframe>
                    </md-whiteframe>
                </div>
            </mu-flexbox-item>
        </mu-flexbox>
      </md-whiteframe>
      </form>

    <md-dialog md-open-from="#custom" md-close-to="#custom" ref="dialog1">

        <md-dialog-content>
            <idclist ref="idclist" @selectform="getuser">
            </idclist>
        </md-dialog-content>

        <md-dialog-actions>
            <md-button class="md-primary" @click.native="closetrueDialog('dialog1')">确认</md-button>
        </md-dialog-actions>
    </md-dialog>

  </div>
</template>

<script>
import idclist from './idclist'

export default {
/* eslint-disable */
    data() {
        return {
            selectip: null,
            output: '',
            deployLoading: false,
            fristactive: true,
            outstatus: {
                color:'gray',
                fontSize: '1.4em',
                des: '未执行',
                ops: '执行构建'
            },
            deploylist: {
                resource: '',
                user: '',
                args: '',
                rediskey: ''
            }
        }
    },
    updated() {
        var ele = document.getElementById('deploylog')
        if (ele) {
            ele.scrollTop = ele.scrollHeight
        }
    },
    methods: {
        openDialog(ref) {
            this.$refs.dialog1.open();
        },
        closefalseDialog(ref) {
            this.$refs.dialog1.close();
            this.selectip = []
        },
        closetrueDialog(ref) {
            this.$refs.dialog1.close();
        },
        getuser(item) {
            this.selectip = item.map(item => item.ip)
        },
        deploy () {
            this.$http.get('http://test.com/yunwei/api/deploy',
            {
                params: {
                    resource:this.deploylist.resource,
                    user:this.deploylist.user,
                    args:this.deploylist.args,
                    serverlist:JSON.stringify(this.selectip)
                }
            }
            ).then(response => {
                if (response.data.ok != false) {
                    var _this = this
                    if (response.data.code != 0) {
                        this.fristactive= false
                        this.outstatus.color = 'red'
                        this.outstatus.des = '执行错误'
                        this.outstatus.ops = '再次构建'
                        _this.output = response.data.msg
                    }
                    else {
                        this.fristactive= false
                        this.outstatus.color = 'green'
                        this.outstatus.des = '执行结果'
                        this.outstatus.ops = '再次构建'
                        this.deploylist.rediskey = response.data.data.rediskey
                        _this.output = this.getdeployresoult()
                    }
                }
            })
        },
        getdeployresoult(resoult) {
            this.$http.get('http://test.com/yunwei/api/deployResoult',
            {
                params: {
                    rediskey:this.deploylist.rediskey,
                    resource:this.deploylist.resource,
                }
            } 
            ).then(response => {
                if (response.data.ok != false) {
                    console.log(response.data)
                    if (this.output === undefined) {
                        this.deployLoading = true
                        this.output = '\n'
                    }
                    if (/Deploy\ End/.test(response.data.msg)) {
                        this.deployLoading = false
                        return
                    }
                    if (response.data.msg && response.data.msg != 'null' ) {
                        this.output = `${this.output}${response.data.msg}\n`
                    }

                    window.setTimeout(() => {
                    this.getdeployresoult()
                    }, 200)
                }
            })
        }
    },
    components: {
        idclist
    }
}
</script>


<style>
</style>
