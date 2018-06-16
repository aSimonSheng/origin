# -*-coding:utf-8-*-
from flask import Blueprint

news_bul = Blueprint('news_bul', __name__, url_prefix='/news')

from . import views