# -*-coding:utf-8-*-
import re
import random
from flask import request, current_app, make_response, json, jsonify, session
from info import redis_store, constants, db
from info.libs.yuntongxun.sms import CCP
from info.models import User
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_bul

# 图片验证码请求
@passport_bul.route('/image_code')
def get_image_code():
    """
    获取请求参数
    生成图片验证码
    保存到redis
    返回图片验证码
    :return: 
    """""
    # 获取用户利用get请求发送的数据cur_id
    cur_id = request.args.get('cur_id')
    prcur_id = request.args.get('prcur_id')
    name, text, image_data = captcha.generate_captcha()
    # 将图片验证码写入到redis中
    try:
        redis_store.set('image_code:%s'%cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)

        if prcur_id:
            redis_store.delete('image_code:%s'%prcur_id)
    except Exception as e:
        current_app.logger.error(e)

    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'

    return response




# 短信验证请求
# 请求路径 /passport.sms_code
# 请求方法 POST
# 请求参数
# 返回值; error, errmag
@passport_bul.route('/sms_code', methods=['POST'])
def get_sms_code():
    """
    获取参数 request.data json.loads(json)
    教研参数是否为空
    验证手机格式
    通过uuid取出图片中的验证码
    判断是否过期
    判断两个图片验证是否相等
    生成短信验证码
    调用云通讯发送(手机号,[验证码,有效期],模板id)
    保存到redis
    返回前端
    :return: 
    """
    # json_data = request.data
    # dict_data = json.loads(json_data)
    dict_data = request.json
    mobile = dict_data.get('mobile')
    image_code = dict_data.get('image_code')
    image_code_id = dict_data.get('image_code_id')

    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 验证手机号格式
    if not re.match(r"1[3456789]\d{9}", mobile):
        #  表示格式错误
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式错误")

    try:
        redis_store_code = redis_store.get('image_code:%s'%image_code_id)
    except Exception as e:
        current_app.logger(e)
        return jsonify(errno=RET.DBERR, errmsg="查找图片验证码失败")

    if not redis_store_code:
        return jsonify(errno=RET.NODATA,errmsg="验证码过期")

    if image_code.lower() != redis_store_code.lower():
        return jsonify(errno=RET.DATAERR,errmsg="验证码输入不正确")

    # 生成验证码
    sms_code = '%06d'%random.randint(0, 999999)
    # 调用云通讯发送
    print(sms_code)
    # ccp = CCP()
    # result = ccp.send_template_sms(mobile, [sms_code, 5], 1)

    # if result == -1:
        # return jsonify(errno=RET.THIRDERR, errmsg="验证码发送失败")

    try:
         redis_store.set('sms_code:%s'%mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="短信保存失败")


    return jsonify(errno=RET.OK,errmsg="发送成功")



### 短信注册
# 请求路径: /passport/register
# 请求方式: POST
# 请求参数: mobile, sms_code,password
# 返回值: errno, errmsg
@passport_bul.route('/register', methods=['POST'])
def register():
    """
    获取参数
    校验参数
    通过手机悍马取出redis中的验证码
    判断是否过期
    判断是否相等
    判断用户对象,设置属性\保存到数据库
    返回前端页面
    :return: 
    """
    dict_data = request.json
    mobile = dict_data.get('mobile')
    sms_code = dict_data.get('sms_code')
    password = dict_data.get('password')

    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    try:
        redis_sms_code = redis_store.get('sms_code:%s'%mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="短信验证码异常")

    if not redis_sms_code:
        return jsonify(errno=RET.NODATA,errmsg="验证码过期")

    if redis_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR,errmsg="验证码错误")

    user = User()
    user.nick_name = mobile
    user.mobile = mobile
    #TODO 未加密
    # user.password_hash = password
    user.password = password

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="用户保存异常")

    return jsonify(errno=RET.OK,errmsg="注册成功")


# 登录界面

# 请求路径: /passport/login
# 请求方式: POST
# 请求参数: mobile,password
# 返回值: errno, errmsg

@passport_bul.route('/login')
def login():
    # 获取参数
    dict_data = request.json
    mobile = dict_data.get('mobile')
    password = dict_data.get('password')

    # 校对参数
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR,errmsg="数据不完整")

    # 通过手机号,获取用户对象
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据库查询异常")


    # 判断用户对象是否存在
    if not user:
        return jsonify(errno=RET.NODATA,errmsg="该用户不存在")

    #判断密码
    if not user.check_passowrd(password):
        return jsonify(errno=RET.DATAERR,errmsg="密码不正确")

    # 记录登录状态
    session['user_id'] = user.id
    session['nick_name'] = user.nick_name
    session['mobile'] = user.mobile

    # 返回前端界面
    return jsonify(errno=RET.OK,errmsg="登录成功")







