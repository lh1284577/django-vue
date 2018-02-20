#coding=utf-8

import paramiko

import subprocess,shlex
from ..data.Redis import Redis

class Paramiko: 

	def __init__(self,ip,user):
		self.ip = ip
		self.port = 22
		self.user = user
	
	def auth(self,rediskey):
		try:
                	if self.user == 'root':
                	        self.private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
                	else:
                        	self.private_key = paramiko.RSAKey.from_private_key_file('/home/%s/.ssh/id_rsa' % user)

			self.transport = paramiko.Transport((self.ip, self.port))
                	self.transport.connect(username=self.user, pkey=self.private_key )
		except:
			Redis.lpush(rediskey,u'%s服务器，用户认证失败或IP没有和跳板机打通ssh' % self.ip)
			Redis.lpush(rediskey,'Deploy End')



	def put(self,file):
		sftp = paramiko.SFTPClient.from_transport(self.transport)
		dfile=file.split('/')[-1]
		sftp.put(file, '/tmp/%s' % dfile)
		 

	def cmd(self,command,rediskey):
		try:
			ssh = paramiko.SSHClient()
        		ssh._transport = self.transport
        		stdout = ssh.exec_command(self.process(command,rediskey))
        		result = stdout.read()
        		print(result)
        		return 'ok'
		except:
			pass


	def process(self,command,rediskey):
		try:
       			bashout = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       			Redis.delete(rediskey)
       			while bashout.poll() is None:  
       			    line = bashout.stdout.readline()  
       			    line = line.strip() 
       			    if line != 'null':
       			        Redis.lpush(rediskey,"%s" % (line))
       			Redis.lpush(rediskey,'Deploy End')
		except:
			pass


	def run(self,file,command,rediskey):
		self.auth(rediskey)
		self.put(file)
		self.cmd(command,rediskey)
		self.close()

	def close(self):
		self.transport.close()

if __name__ == '__main__':
	a = Paramiko('localhost','root')
	print a.run('/tmp/lihao.sh','bash /opt/lihao.sh','bash.deploy.6251003703')
	print a.process('df','bash.deploy.6251003703')
