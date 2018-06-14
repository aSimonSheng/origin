# -*-coding:utf-8-*-
from info import redis_store # 调用全局化的redis_store
from info.models import User
from info.utils.response_code import RET
from . import blueprint
from flask import render_template, current_app, session, jsonify


@blueprint.route('/')
def hello_word():
    # 获取用户编号
    user_id = session.get('user_id')

    #查询用户对象
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    # 返回页面到模板界面
    data = {
        "user_info":user.to_dict() if user else  None
    }
    return  render_template("news/index.html", data = data)



    return render_template('news/index.html')


@blueprint.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file('news/favicon.ico')