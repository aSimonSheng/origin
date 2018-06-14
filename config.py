# -*-coding:utf-8-*-
import redis
import logging
class Config(object):
    # 普通配置
    DEBUG = True
    SECRET_KEY = 'akdjhaidiagdgag'

    #数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.223.140:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    #redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = 6379

    # 配置session信息
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True #session签字存储(签字代表秘钥)
    SESSION_REDIS = redis.StrictRedis(REDIS_HOST, REDIS_POST)
    PERMANENT_SESSION_LIFETIME = 3600*24*2 # 设置session有效期

    # 控制日志输出等级
    LEVEL = logging.DEBUG


# 开发模式
class DeveloperConfig(Config):
    pass

# 生产模式
class ProductConfig(Config):
    DEBUG = False
    LEVEL = logging.ERROR
    pass

#测试模式
class TestingConfig(Config):
    pass

config_dict = {
    'develop':DeveloperConfig,
    'product':ProductConfig,
    'testing':TestingConfig
}