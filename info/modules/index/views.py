# -*-coding:utf-8-*-
from info import redis_store # 调用全局化的redis_store
from . import blueprint
@blueprint.route('/')
def hello_word():

    redis_store.set('name','SimonSheng')
    name = redis_store.get('name')
    print(name)
    # session['name'] = 'zhagnsan'
    # 使用current_app输出显示日志,并通过设置输出等级控制消息的输出
    # current_app.logger.debug('调试信息')
    # current_app.logger.info('调试信息')
    # current_app.logger.warn('调试信息')
    # current_app.logger.error('调试信息')

    return 'hello Word'