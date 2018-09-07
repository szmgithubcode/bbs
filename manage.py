#encoding: utf-8

from flask_migrate import Migrate,MigrateCommand
from zlktqademo import app
from flask_script import Manager
from exts import db
import config
from models import UserModel,QuestionModel,AnswerModel

app.config.from_object(config)
db.init_app(app)

#创建命令管理器
manager = Manager(app)
# 绑定app到db
migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

#模型----迁移文件-----表
#本地新建数据库zlktqademo
#python manage.py db init(创建目录)
#python manage.py db migrate（迁移文件）
#python manage.py db upgrade（创建表）

if __name__ == "__main__":
    manager.run()


