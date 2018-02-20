#coding=utf-8
from base import APBase

class Redis(object):
	'添加list数据'
        @staticmethod
        def lpush(redisKey,data):
            try:
                redisConn = APBase.getRedisConnection()
                redisConn.lpush(redisKey, data)
                redisConn = None
            except:
                return False

        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection()
                data = redisConn.delete(redisKey)
                redisConn = None
		return data
            except:
                return False

        @staticmethod
        def rpop(redisKey):
            try:
                redisConn = APBase.getRedisConnection()
                data = redisConn.rpop(redisKey)
                redisConn = None
		return data
            except:
                return False

if __name__ == '__main__':
	redis = Redis()
     	print Redis.lpush('ares.fl.deploy.test.1.3.5','123')
