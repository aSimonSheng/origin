# -*-coding:utf-8-*-
from flask import Blueprint

#创建首页蓝图对象
blueprint = Blueprint('blueprint', __name__)

from . import views