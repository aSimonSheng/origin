# -*-coding:utf-8-*-
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from config import config_dict

# 创建db对象
db = SQLAlchemy()

def creat_app(ConfigDict):
    app = Flask(__name__)

    # 通过对config的引用,传入参数,控制响应的环境
    config = config_dict[ConfigDict]

    app.config.from_object(config)

    # 初始化db
    db.init_app(app)

    # 创建redis对象
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_POST, decode_responses=True)

    # 创建session对象
    Session(app)

    # 设置csrf保护
    CSRFProtect(app)

    return app