# -*-coding:utf-8-*-
import logging
from flask import current_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from info import creat_app, db

app = creat_app('product')

# 设置迁移命令
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)


@app.route('/')
def hello_word():

    # redis_store.set('name','SimonSheng')
    # name = redis_store.get('name')
    # print(name)
    # session['name'] = 'zhagnsan'
    # 使用current_app输出显示日志,并通过设置输出等级控制消息的输出
    current_app.logger.debug('调试信息')
    current_app.logger.info('调试信息')
    current_app.logger.warn('调试信息')
    current_app.logger.error('调试信息')


    return 'hello Word'

if __name__ == '__main__':
    manage.run()