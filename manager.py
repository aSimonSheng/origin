# -*-coding:utf-8-*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

app = Flask(__name__)

class Config(object):
    # 普通配置
    DEBUG = True

    #数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.223.140/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_POST = 6379


app.config.from_object(Config)

#创建db对象
db = SQLAlchemy(app)

#创建redis对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_POST,decode_responses=True)


@app.route('/')
def hello_word():

    redis_store.set('name','SimonSheng')
    name = redis_store.get('name')
    print(name)

    return 'hello Word'

if __name__ == '__main__':
    app.run()