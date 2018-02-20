#!/usr/bin/env python
# -*- coding:utf-8 -*-
import paramiko
 
class SSHConnection(object):
 
    def __init__(self, host='localhost', port=8222, username='root',pwd='rootROOT123'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None
 
    def run(self):
        self.connect()  # 连接远程服务器
        self.upload('/tmp/lihao.sh','/opt/lihao.sh')  # 将本地的db.py文件上传到远端服务器的/tmp/目录下并改名为1.py
        self.cmd('df')  # 执行df 命令
        self.close()    # 关闭连接
 
    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport
 
    def close(self):
        self.__transport.close()
 
    def upload(self,local_path,target_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path,target_path)
 
    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print(result)
        return result
 
obj = SSHConnection()
obj.run()
