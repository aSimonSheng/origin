# -*-coding:utf-8-*-
from info import redis_store, constants  # 调用全局化的redis_store
from info.models import User, News, Category
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

    # 查询数据库,安好点击量,前10 条新闻
    try:
        clicl_news = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)


    # 将对象列表壮汉成字典列表
    clicl_news_list = []
    for news in clicl_news:
        clicl_news_list.append(news.to_dict())


    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)

    category_list = []
    for cate in categories:
        category_list.append(cate.to_dict())






    # 返回页面到模板界面
    data = {
        "user_info":user.to_dict() if user else  None,
        'clicl_news_list':clicl_news_list,
        'category_list':category_list,
    }
    return  render_template("news/index.html", data = data, )



    return render_template('news/index.html')


@blueprint.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file('news/favicon.ico')