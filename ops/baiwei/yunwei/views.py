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
import shlex
from .data.Redis import Redis
import random
import multiprocessing
from  utils.Paramiko import Paramiko
from utils.Ansible import AnsibleTask
from utils.Subprocess import Subprocess

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


subprocess = Subprocess()

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

def upload(request):
	if request.method == 'OPTIONS':
		return HttpResponse('ok')
    	if request.method == "POST":
    	    myFile =request.FILES.get("file", None)
    	    destination = open(os.path.join("/tmp/",myFile.name),'wb+')
    	    for chunk in myFile.chunks():
    	        destination.write(chunk)  
    	    destination.close()  
    	    return JsonResponse({'msg':'执行成功','code':0})


def rsyncFile(request):
        if request.method == 'OPTIONS':
                return HttpResponse('ok')
	if request.method == "POST":
		data = json.loads(request.body)	
		iplist = eval(data['iplist'])
		rsyncfilelist = eval(data['filelist'])
		localfilelist = eval(data['localfilelist'])
		des = data['des']
		user = data['user']
		filelist = []
		serverlist = {}
		if rsyncfilelist != []:
			filelist = rsyncfilelist 
		elif localfilelist != '':
			filelist.append(localfilelist.split('/')[-1])
		for ip in iplist:
			paramiko = Paramiko(ip,user)
			out = paramiko.auth('rsyncFile')
			if out is False:
				serverlist[ip] = -1
			else:
				serverlist[ip] = {'status':'-1','color':'','percent':'','progress':''}
		out = subprocess.rsyncfile(serverlist,filelist,des,user)	
		if out is True:
			return JsonResponse({'msg':'ok','code':0})
		else:	
			return JsonResponse({'msg':'执行失败','code':400})


def rsyncFileResoult(request):
        if request.method == 'OPTIONS':
                return HttpResponse('ok')
        if request.method == "POST":
                data = json.loads(request.body)
                iplist = eval(data['iplist'])
		serverlist = {}
		for ip in iplist:
			out = subprocess.progressbar(ip)
                        serverlist[ip] = {'status':'-1','color':'','percent':'','progress':out}
		return JsonResponse({'msg':serverlist,'code':0})


def lsDir(request):
        if request.method == "GET":
		dir = request.GET['dir']
		out = os.popen('ls -l %s' % dir).readlines()
		print "=========%s" % out
		return JsonResponse({'msg':out,'code':0})
