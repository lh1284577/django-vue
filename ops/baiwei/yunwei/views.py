#coding=utf-8
import os
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django import forms
import datetime,time
import json
from yunwei.serializers import AESSLISTSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from yunwei.models import AESSLIST
import sys
import subprocess,shlex
from .data.Redis import Redis
import random
import multiprocessing
from  utils.Paramiko import Paramiko
from utils.Ansible import AnsibleTask


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class AESSLISTViewSet(viewsets.ModelViewSet):
        queryset = AESSLIST.objects.all()
        serializer_class = AESSLISTSerializer


def deploy(request):
	serverlist = request.GET['serverlist']
	resource = request.GET['resource']
	args = request.GET['args']
	user = request.GET['user']

	ran = random.uniform(10, 20)
	key = str(ran).split('.')[-1]
	
        if  resource == '' or user == '':
                return JsonResponse({'msg':'参数不完整','code':400})

        if os.path.isdir(resource) or not os.path.exists(resource):
		return JsonResponse({'msg':'%s 是一个目录或者文件不存在' % resource,'code':400})

	elif resource.split('.')[-1] == 'sh':
		if serverlist == '[]' or serverlist == 'null':
			return JsonResponse({'msg':'未选择服务器','code':400})

		dfile = '/tmp/' + resource.split('/')[-1]
		if args == '':
                	shell_cmd = 'bash %s' % (dfile)
		else:
			shell_cmd = 'bash %s %s' % (dfile,args)
                cmd = shlex.split(shell_cmd)
		rediskey='bash.deploy.%s' % key
		'''异步执行'''
		serverlist = eval(serverlist)
		for ip in serverlist:
        		dprocess = multiprocessing.Process(target = run,args=(ip,user,cmd,resource,rediskey))
        		dprocess.start()

		return JsonResponse({'msg':'执行成功','data':{'rediskey':rediskey},'code':0})
	elif resource.split('.')[-1] == 'py':
		if serverlist == '[]' or serverlist == 'null':
			return JsonResponse({'msg':'未选择服务器','code':400})
		dfile = '/tmp/' + resource.split('/')[-1]
                if args == '':
                        python_cmd = 'python %s' % (dfile)
                else:
                        python_cmd = 'python %s %s' % (dfile,args)
                cmd = shlex.split(python_cmd)
                rediskey='python.deploy.%s' % key
                '''异步执行'''
                serverlist = eval(serverlist)
                for ip in serverlist:
                        dprocess = multiprocessing.Process(target = run,args=(ip,user,cmd,resource,rediskey))
                        dprocess.start()

                return JsonResponse({'msg':'执行成功','data':{'rediskey':rediskey},'code':0})

	elif resource.split('.')[-1] == 'yml':
		playbook_file = [resource]
		playbook_vars = eval(args)
		rediskey='ansible.deploy.%s' % key
		Ans = AnsibleTask(rediskey,playbook_vars,playbook_file)
		Ans.ansiblePlay()
		Ans.run()

		return JsonResponse({'msg':'执行成功','data':{'rediskey':rediskey},'code':0})
	else:
		return JsonResponse({'msg':'%s 不是一个可执行脚本(python/bash/yml)' % resource,'code':400})

'''
bash和python脚本执行调用
'''
def run(ip,user,cmd,resource,rediskey):
	paramiko = Paramiko(ip,user)
	cmd = ' '.join(cmd)
        out = paramiko.run(resource,cmd,rediskey)
	


def deployResoult(request):
	rediskey = request.GET['rediskey']
	out = Redis.rpop(rediskey)
        return JsonResponse({'msg':out,'code':0})
