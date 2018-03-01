from flask import Blueprint, render_template, flash, url_for, redirect
from jobplus.forms import LoginForm, UserRegisterForm, CompanyRegisterForm
from jobplus.models import db, User, CompanyInfo, Job, Resume, JobExperience, EduExperience, ProjectExperience
from flask_login import login_user, login_required, logout_user

front = Blueprint('front', __name__)

#主页
@front.route('/')
def index():
    hot_companys = CompanyInfo.query.order_by(CompanyInfo.views_count.desc()).limit(8)
    hot_jobs = Job.query.order_by(Job.views_count.desc()).limit(10)
    return render_template('index.html', hot_companys=hot_companys, hot_jobs=hot_jobs)

#登录
@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_disable:
            flash(u'用户已经禁用', 'warning')
            return redirect(url_for('front.login'))
        login_user(user, form.remember_me.data)
        flash(u'登录成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('login.html', form=form)

#注销
@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'注销成功', 'success')
    return redirect(url_for('front.index'))

#企业注册
@front.route('/companyRegister', methods=['GET', 'POST'])
def company_register():
    form = CompanyRegisterForm()
    if form.validate_on_submit():
        user = form.create_user()
        user.role = User.ROLE_COMPANY
        #添加公司user都应的companyinfo
        company = CompanyInfo(company_name=form.company_name.data, website=form.website.data)
        user.detail = company
        db.session.add(user)
        db.session.commit()
        flash(u'企业注册成功', 'success')
        login_user(user)
        return redirect(url_for('front.index'))
    return render_template('company_register.html', form=form)

#求职者注册
@front.route('/userRegister', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        user = form.create_user()
        flash(u"注册成功", 'success')
        login_user(user)
        return redirect(url_for('front.index'))
    return render_template('user_register.html', form=form)


