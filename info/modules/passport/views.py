# -*-coding:utf-8-*-
from flask import request

from info import redis_store
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
    cur_id = request.args.get('cur_id')
    name, text, image_data = captcha.generate_captcha()

    return image_data