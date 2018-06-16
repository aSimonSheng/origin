# -*-coding:utf-8-*-
from . import news_bul
from flask import render_template

@news_bul.route('/<int:news_id>')
def news_detil(news_id):


    return render_template('news/detail.html', data = {})