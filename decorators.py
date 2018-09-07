#encoding: utf-8
from functools import wraps
import flask

#判断是否登录
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if hasattr(flask.g,'user'):
            return func(*args,**kwargs)
        else:
            return flask.redirect(flask.url_for('login'))

    return wrapper

