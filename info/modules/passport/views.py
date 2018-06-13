# -*-coding:utf-8-*-
from flask import request, current_app

from info import redis_store, constants
from info.constants import IMAGE_CODE_REDIS_EXPIRES
from info.utils.captcha.captcha import captcha
from . import passport_bul

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


    return image_data