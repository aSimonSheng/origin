# -*-coding:utf-8-*-
from info import redis_store # 调用全局化的redis_store
from . import blueprint
from flask import render_template, current_app


@blueprint.route('/')
def hello_word():

    return render_template('news/index.html')


@blueprint.route('/favicon.ico')
def web_logo():
    return current_app.send_static_file('news/favicon.ico')