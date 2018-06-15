# -*-coding:utf-8-*-
from info import redis_store, constants  # 调用全局化的redis_store
from info.models import User, News, Category
from info.utils.response_code import RET
from . import blueprint
from flask import render_template, current_app, session, jsonify, request


# 首页新闻列表
# 请求路径:/newslist
# 请求方式:GET
# 请求参数:cid, page,per_page
# 返回值:data数据
@blueprint.route('/newslist')
def new_list():
    """
    1,获取参数
    2,校验参数,转换参数类型
    3,根据条件查询数据
    4,将查询到的分类对象数据,转换成字典
    5,返回请求数据
    :return: 
    """
    cid = request.args.get('cid')
    page = request.args.get('page',1)
    per_page = request.args.get('per_page', 10)

    # 校验参数,转换参数类型
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1
        per_page = 10

    # 根据条件查询
    try:
        # 判断分类条件编号不为1
        filter = []
        if cid != 1:
            filter.append(News.category_id == cid)
            # 查询
        paginate = News.query.order_by(News.create_time.desc()).paginate(page, per_page, False) #这里获取的是一个分页对象
        # 获取分页中的内容, 总页数, 当前页, 当前页的所有对象
        totalPage = paginate.pages
        currentPage = paginate.page
        items = paginate.items
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据查询失败")

    # 将查询的分类对象转成字典
    newsList = []
    for new in items:
        newsList.append(new.to_dict())

    # 返回数据

    return jsonify(errno=RET.OK,errmsg="获取数据成功", cid = cid, totalPage = totalPage, currentPage = currentPage, newsList = newsList)



@blueprint.route('/')
def index():
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