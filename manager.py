# -*-coding:utf-8-*-
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

class Config(object):
    # 普通配置
    DEBUG = True
    SECRET_KEY = 'akdjhaidiagdgag'

    #数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.223.140/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = 6379

    # 配置session信息
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True #session签字存储(签字代表秘钥)
    SESSION_REDIS = redis.StrictRedis(REDIS_HOST, REDIS_POST)
    PERMANENT_SESSION_LIFETIME = 3600*24*2 # 设置session有效期


app.config.from_object(Config)

#创建db对象
db = SQLAlchemy(app)

#创建redis对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_POST,decode_responses=True)

#创建session对象
Session(app)

#设置csrf保护
CSRFProtect(app)


@app.route('/')
def hello_word():

    # redis_store.set('name','SimonSheng')
    # name = redis_store.get('name')
    # print(name)
    session['name'] = 'zhagnsan'

    return 'hello Word'

if __name__ == '__main__':
    app.run()