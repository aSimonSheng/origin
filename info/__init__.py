# -*-coding:utf-8-*-
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from config import config_dict
from info.modules.index import blueprint

# 创建db对象
db = SQLAlchemy()

# 指定redis_store为全局变量
redis_store = None

def creat_app(ConfigDict):
    # # 日志模块方法的调用
    # log_file()

    app = Flask(__name__)

    # 通过对config的引用,传入参数,控制响应的环境
    config = config_dict[ConfigDict]

    # 调用日志方法
    log_file(config.LEVEL)

    app.config.from_object(config)

    # 初始化db
    db.init_app(app)

    # 创建redis对象
    global redis_store
    redis_store = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_POST, decode_responses=True)

    # 创建session对象
    Session(app)

    # 设置csrf保护
    CSRFProtect(app)

    # 注册首页蓝图
    app.register_blueprint(blueprint)

    return app

#日志文件,作用:用来记录程序的运行过程,比如:调试信息,接口访问信息,异常信息
def log_file(level):
    # 设置日志的记录等级,设置日志等级: 常见等级有:DEBUG < INFO < WARING < ERROR < FATAL(CRITICAL)
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件编号
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)