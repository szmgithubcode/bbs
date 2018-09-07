#encoding: utf-8

from flask import Flask
from exts import db
import flask
import config
from models import UserModel,QuestionModel,AnswerModel
from decorators import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    context = {
        'questions': QuestionModel.query.order_by('-create_time').all()
    }
    return flask.render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        telephone = flask.request.form.get('telephone')
        password = flask.request.form.get('password')
        user = UserModel.query.filter_by(telephone=telephone).first()
        if user and user.check_password(password):
            flask.session['id'] = user.id
            #如果想在31天内都不需要登录
            flask.session.permanent = True
            return flask.redirect(flask.url_for('index'))
        else:
            return '<script>alert("用户名或密码错误"); window.history.back();</script> '

@app.route('/logout/',methods=['GET'])
def logout():
	#flask.session.pop('user_id')
	#del flask.session['user_id']
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if flask.request.method == 'GET':
        return flask.render_template('regist.html')
    else:
        telephone=flask.request.form.get('telephone')
        username=flask.request.form.get('username')
        password1=flask.request.form.get('password1')
        password2=flask.request.form.get('password2')
        user=UserModel.query.filter(UserModel.telephone==telephone).first()
        if user:
            return '<script>alert("该手机号码已被注册，请更换手机号码！"); window.history.back();</script> '
        else:
            if password1!=password2:
                return '<script>alert("两次密码不相等，请核对后再填写！"); window.history.back();</script> '
            else:
                user = UserModel(telephone = telephone, username = username, password = password1)
                db.session.add(user)
                db.session.commit()
                return flask.redirect(flask.url_for('login'))

@app.route('/d/<id>/')
def detail(id):
    question_model = QuestionModel.query.filter(QuestionModel.id == id).first()
    return flask.render_template('detail.html', question=question_model)

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if flask.request.method == 'GET':
        return flask.render_template('question.html')
    else:
        title = flask.request.form.get('title')
        content = flask.request.form.get('content')
        if title and content:
            question_model = QuestionModel(title=title, content=content)
            #通过g对象代替：
            #user_id=session['user_id']
            # user=UserModel.query.filter(UserModel.id==user_id).first()
            question_model.author = flask.g.user
            db.session.add(question_model)
            db.session.commit()
            return flask.redirect(flask.url_for('index'))
        else:
            return '<script>window.history.back();</script> '

@app.route('/comment/',methods=['POST'])
@login_required
def comment():
    question_id = flask.request.form.get('question_id')
    content = flask.request.form.get('content')
    if content:
        answer_model = AnswerModel(content=content)
        #通过g对象代替：
        #user_id=session['user_id']
        # user=UserModel.query.filter(UserModel.id==user_id).first()
        answer_model.author = flask.g.user
        answer_model.question = QuestionModel.query.filter(QuestionModel.id == question_id).first()
        db.session.add(answer_model)
        db.session.commit()
        return flask.redirect(flask.url_for('detail', id = question_id))
    else:
        return '<script>window.history.back();</script> '

@app.route('/search/')
def search():
    q = flask.request.args.get('q')
    questions = QuestionModel.query.filter(or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q)))
    context = {
        'questions': questions
    }
    return flask.render_template('index.html', **context)

#优化替代comment（）中user_id=session['user_id']、 user=UserModel.query.filter(UserModel.id==user_id).first()
#优化替代question()中user_id=session['user_id']、 user=UserModel.query.filter(UserModel.id==user_id).first()
#先执行钩子函数再执行装饰器
@app.before_request
def before_request():
    id = flask.session.get('id')
    if id:
        user = UserModel.query.filter(UserModel.id == id).first()
        flask.g.user = user

#登录成功后，首页和发布问答两个页面都有用户名、注销。(上下文模板渲染)
@app.context_processor
def context_processor():
	# user_id=flask.session.get('user_id')
    # if user_id:
    #     user=UserModel.query.filter(UserModel.id==user_id).first()
    #     if user:
    #         return  {'user':user}
    # return {}
    if hasattr(flask.g, 'user'):
        return {"user": flask.g.user}
    return {}

if __name__ == '__main__':
    #app.run(port=7000)
    app.run()