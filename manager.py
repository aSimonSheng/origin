# -*-coding:utf-8-*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.223.140/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app.config.from_object(Config)

#创建db对象
db = SQLAlchemy(app)

@app.route('/')
def hello_word():
    return 'hello Word'

if __name__ == '__main__':
    app.run(debug=True)