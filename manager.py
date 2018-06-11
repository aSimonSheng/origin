# -*-coding:utf-8-*-
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)

from config import Config
app.config.from_object(Config)

#创建db对象
db = SQLAlchemy(app)

#创建redis对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_POST,decode_responses=True)

#创建session对象
Session(app)

#设置csrf保护
CSRFProtect(app)

# 设置迁移命令
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)


@app.route('/')
def hello_word():

    # redis_store.set('name','SimonSheng')
    # name = redis_store.get('name')
    # print(name)
    session['name'] = 'zhagnsan'

    return 'hello Word'

if __name__ == '__main__':
    manage.run()