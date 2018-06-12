# -*-coding:utf-8-*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from info import creat_app, db


app = creat_app('product')

# 设置迁移命令
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)




if __name__ == '__main__':
    manage.run()