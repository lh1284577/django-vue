
  欢迎来到Django的世界，陪着我一起学习丰富此平台吧


# 是时候一起学习下一个知识点了

# 安裝套件
	docker1.12+
	docker-compose1.12+

### docker-compose安装
	curl -L https://github.com/docker/compose/releases/download/1.13.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
	chmod +x /usr/local/bin/docker-compose
	运行： docker-compose up -d


# 这篇可以学到什么

	1.通过vue+django 前后端分离方式完成平台建设
	2.通过ansible+redis 做异步处理，回调渲染
	3.利用multiprocessing 同样可以做到异步处理，回调渲染
	4.利用类可视化视图轻松完成CRUD操作

### 默认安装
由于此次需要nginx服务，所以需要小伙伴将80端口映射到本机电脑(我相信你可以)
默认提供域名为： test.com

## 实际体验
我提供了3个测试脚本分别是：
/opt/目录下的： lihao.py , lihao.sh , lihao.yml

### 顺便说一下，cmdb_fe是我的vue源码，也是刚开始写，有兴趣还请多指教


### 成功访问就会是这样：
![Image text](https://github.com/lh1284577/django-vue/blob/master/%E9%85%8D%E5%9B%BE.png)
