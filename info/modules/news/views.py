# -*-coding:utf-8-*-
from info import constants, db
from info.models import User, News, Comment, CommentLike
from info.utils.commen import user_login_data
from info.utils.response_code import RET
from . import news_bul
from flask import render_template, session, current_app, jsonify, g, abort, request

# 点赞与取消点赞
# 请求路径: /news/comment_like
# 请求方式: POST
# 请求参数:news_id,comment_id,action,g.user
# 返回值: errno,errmsg
@news_bul.route('/comment_like', methods=['POST'])
@user_login_data
def comment_like():
    # 判断用户是否登录
    # 获取参数
    # 校验参数
    # 根据惭怍类型,执行具体操作
    # 返回响应
    if not g.user:
        return jsonify(errno=RET.NODATA,errmsg="用户为登录")

    dict_data = request.json
    news_id = dict_data.get('news_id')
    comment_id = dict_data.get('comment_id')
    action = dict_data.get('action')

    if not all ([news_id, comment_id, action]):
        return jsonify(errno=RET.NODATA,errmsg="数据参数不完整")

    if not action in ['add', 'remove']:
        return jsonify(errno=RET.DATAERR,errmsg="操作类型有误")

    # 取出评论对象
    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)

    if not comment:
        return jsonify(errno=RET.NODATA,errmsg="评论不存在")

    if action == 'add':
        comment_like = CommentLike.query.filter(CommentLike.comment_id == comment_id,CommentLike.user_id == g.user.id),all()
        if  not comment_like:
            comment_like = CommentLike()
            comment_like.comment_id = comment_id
            comment_like.user_id = g.user.id
            db.session.add(comment_like)

            # 点赞数量+1
            comment.like_count += 1
    else:
        comment_like = CommentLike.query.filter(CommentLike.comment_id == comment_id,CommentLike.user_id == g.user.id), all()
        if comment_like:
            db.session.delate(comment_like)
            comment.like_count -= 1

    return jsonify(errno=RET.OK,errmsg="操作完成")








# 新闻评论
# 请求路径: /news/news_comment
# 请求方式: POST
# 请求参数:news_id,comment,parent_id, g.user
# 返回值: errno,errmsg,评论字典
@news_bul.route('/news_comment', methods=['POST'])
@user_login_data
def news_comment():
    if not g.user:
        return jsonify(errno=RET.USERERR,errmsg="用户未登陆")

    dict_data = request.json
    news_id = dict_data.get('news_id')
    content = dict_data.get('comment')
    parent_id = dict_data.get('parent_id')

    if not all ([news_id,content]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")

    comment = Comment()
    comment.user_id = g.user.id
    comment.news_id = news_id
    comment.content = content

    if parent_id:
        comment.parent_id = parent_id

    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="评论失败")

    return jsonify(errno=RET.OK,errmsg="评论成功", data=comment.to_dict())



# 新闻收藏与取消收藏
# 请求路径: /news/news_collect
# 请求方式: POST
# 请求参数:news_id,action, g.user
# 返回值: errno,errmsg
@news_bul.route('/news_collect', methods=['POST'])
@user_login_data
def news_collect():
    """
    1判断用户是否登录
    2.获取参数
    3.校验参数
    4,根据操作类型,收藏或取消收藏
    5响应操作
    :return: 
    """
    if not g.user:
        return jsonify(errno=RET.NODATA,errmsg="用户未登录")

    dict_data = request.json
    news_id = dict_data.get('news_id')
    action = dict_data.get('action')

    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不完整")

    if not action in ['collect','cancel_collect']:
        return jsonify(errno=RET.DATAERR,errmsg="操作类型错误")

    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)

    if not news:
        return jsonify(errno=RET.NODATA,errmsg="该新闻不存在")

    if action == "collect":
        g.user.collection_news.append(news)
    else:
        g.user.collection_news.remove(news)

    return jsonify(errno=RET.OK,errmsg="操作成功")




# 新闻详情
@news_bul.route('/<int:news_id>')
@user_login_data
def news_detil(news_id):

    try:
        click_news = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for new in click_news:
        click_news_list.append(new.to_dict())

    # 新闻内容的展示
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)

    # 如果没有新闻,返回404
    if not news:
        abort(404)

    # 判断用户是否收藏该新闻
    is_collected = False
    if g.user and news in g.user.collection_news:
        is_collected = True

    # 查询新闻评论
    try:
        comments = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)

    # 查询用户对当前用户的哪些评论点赞
    if g.user:
        # 得到当前新闻用户点赞的所有编号
        # 获取所有评论编号
        comment_ids = [comm.id for comm in comments]

        # 获取点赞过的所有点赞对象
        my_like_list = CommentLike.query.filter(CommentLike.comment_id.in_(comment_ids),CommentLike.user_id == g.user.id).all()
        # 得到点赞的所有评论编号
        my_like_comment_ids = [com_like.comment_id for com_like in my_like_list]

    #评论对象里边装换成指点列表
    comment_list = []
    for comment in comments:

        com_dict = comment.to_dict()
        com_dict['is_like'] = False
        if g.user and comment.id in my_like_comment_ids:
            com_dict['is_like'] = True

        comment_list.append(com_dict)


    # 拼接数据
    data = {
        "user_info": g.user.to_dict() if g.user else None,
        "click_news_list": click_news_list,
        'news':news.to_dict(),
        'is_collected':is_collected,
        'comments':comment_list,
    }

    return render_template('news/detail.html', data = data)