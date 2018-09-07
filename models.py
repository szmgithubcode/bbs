#encoding: utf-8

from exts import db
from werkzeug.security import generate_password_hash,check_password_hash
import datetime

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __init__(self,*args,**kwargs):
        password = kwargs.get('password')
        username = kwargs.get('username')
        telephone = kwargs.get('telephone')
        self.password = generate_password_hash(password)
        self.username = username
        self.telephone = telephone

    def check_password(self,rawpwd):
        return check_password_hash(self.password, rawpwd)

class QuestionModel(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    author = db.relationship('UserModel',backref='questions')

class AnswerModel(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.id'))
    #主键应和外键字段保持一致。
    # interger类型，用string类型python manage.py db upgrade时报1215错误
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    question = db.relationship('QuestionModel',backref=db.backref('answers',order_by=create_time.desc()))
    author = db.relationship('UserModel',backref='answers')