# -*-coding:utf-8-*-
from info import constants
from info.models import User, News
from info.utils.commen import user_login_data
from info.utils.response_code import RET
from . import news_bul
from flask import render_template, session, current_app, jsonify, g


# 用户登录
@news_bul.route('/<int:news_id>')
@user_login_data
def news_detil(news_id):

    try:
        click_news = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news in click_news:
        click_news_list.append(news.to_dict())

    # 拼接数据
    data = {
        "user_info": g.user.to_dict() if g.user else None,
        "click_news_list": click_news_list,
    }

    return render_template('news/detail.html', data = data)