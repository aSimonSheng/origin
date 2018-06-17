# -*-coding:utf-8-*-
from info.models import User
from info.utils.commen import user_login_data
from info.utils.response_code import RET
from . import news_bul
from flask import render_template, session, current_app, jsonify, g


@news_bul.route('/<int:news_id>')
@user_login_data
def news_detil(news_id):

    # # 获取哟用户编号
    # user_id = session.get('user_id')
    #
    # # 通过编号获取用户对象 通过session中存储的用户登录状态,判断目前用户是否登录.
    # user = None
    # if user_id:
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)

    # 拼接数据
    data = {
        "user_info": g.user.to_dict() if g.user else None
    }

    return render_template('news/detail.html', data = data)