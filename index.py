# -*-coding:utf-8-*-
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import redis
# from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.223.140:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    SECRET_KEY = 'akjfgaug+adgqagargr+jeytjg+agadharya+arhryqar'







app.config.from_object(Config)

db = SQLAlchemy(app)
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# CSRFProtect(app)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()