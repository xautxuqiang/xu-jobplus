from flask import Blueprint, render_template

front = Blueprint('front', __name__)

#主页
@front.route('/')
def index():
    return render_template('index.html')

#登录
@front.route('/')
def login():
    return render_template('login.html')

#企业注册
@front.route('/')
def company_register():
    return render_template('company_register.html')

#求职者注册
@front.route('/')
def user_register():
    return render_template('user_register.html')


