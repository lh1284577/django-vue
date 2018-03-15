# -*- coding=utf-8 -*-
'''
应用基类（每次应用启动时，都必须调用基类的初始化方法）
'''
import redis
import socket
class APBase(object):

    @staticmethod
    def getRedisConnection():
        '''根据数据源标识获取Redis连接池'''
	redisip = socket.gethostbyname('redis')
#	redisip = socket.gethostbyname('127.0.0.1')
        redis.ConnectionPool(port='6379')
        connection = redis.Redis()
        return connection

if __name__ == '__main__':
	apbase=APBase()
	print apbase.getRedisConnection()
