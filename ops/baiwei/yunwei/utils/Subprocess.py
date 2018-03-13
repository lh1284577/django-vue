#!/usr/bin/env python
# -*- coding:utf-8 -*-

import multiprocessing
import subprocess
import shutil
import os
import re
import linecache


class Subprocess:
	
	def __init__(self):
		pass
	
	def process(self,command):
		bashout = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	
	def run(self,command):
		dprocess = multiprocessing.Process(target = self.process,args=(command,))
		dprocess.start()
		return
	
	def rsyncfile(self,iplist,filelist,des,user):
		if os.path.isdir('/tmp/rsyncfiletemp') is True:
			shutil.rmtree('/tmp/rsyncfiletemp')
			os.mkdir('/tmp/rsyncfiletemp')
		else:
			os.mkdir('/tmp/rsyncfiletemp')
		
		filelist = ['/tmp/' + i for i in filelist ]
		filelist = ' '.join(filelist)
		for ip in iplist.keys():
			print "===============%s" % iplist[ip]
			if iplist[ip] == -1:
				self.run('echo "error" > /tmp/rsyncfiletemp/%s.log &' % ip)
			else:
				print('rsync -av --progress  -e "ssh  -o PubkeyAuthentication=yes   -o stricthostkeychecking=no"  %s %s@%s:%s > /tmp/rsyncfiletemp/%s.log &' % (filelist,user,ip,des,ip))
				self.run('rsync -av --progress  -e "ssh  -o PubkeyAuthentication=yes   -o stricthostkeychecking=no"  %s %s@%s:%s > /tmp/rsyncfiletemp/%s.log &' % (filelist,user,ip,des,ip))
		return True
	
	def progressbar(self,ip):
		progressbar = []
		filelist = '/tmp/rsyncfiletemp/%s.log' % ip
		with open(filelist) as file:
			f = file.readlines()
			out = ''.join(f)

		if re.search('error',out):
			return 999


		elif re.search('total size is',out):
			return 100
		
		try:
			f = f[2].split('\r')[-1]
			f = re.search(' (\d+)%',f).group(1).strip()
		except:
			return 0
		return f
