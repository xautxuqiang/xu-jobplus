from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash, abort
from flask_login import current_user
from jobplus.models import User, db, Job, CompanyInfo, Delivery, Resume
from werkzeug.utils import secure_filename
import os
from jobplus.forms import UserInfoForm, PasswordEditForm, ResumeOnlineJobEditForm, ResumeOnlineEduEditForm, ResumeOnlineProEditForm

user = Blueprint('user', __name__, url_prefix='/user')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user.route('/<int:user_id>/userinfo', methods=['GET', 'POST'])
def userinfo(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    if request.method == 'POST':
       if 'file' not in request.files:
           flash(u'没有文件')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           flash(u'没有选择的文件')
           return redirect(request.url)
       if file and allowed_file(file.filename):
           image_type = file.filename.rsplit('.', 1)[1]
           image_name = file.filename.rsplit('.', 1)[0]
           filename = secure_filename('.'.join((image_name,image_type)))
           file_path = os.path.join(current_app.config['USER_LOGO_FOLDER'], current_user.email)
           if not os.path.exists(file_path):
               os.makedirs(file_path, 0o755)
           file.save(os.path.join(file_path, filename))
           #存储用户logo的文件位置
           user.logo = '/static/user/' + current_user.email + '/' + filename
           db.session.add(user)
           db.session.commit()
           return redirect(url_for('user.userinfo', user_id=current_user.id))
    return render_template('user/userInfo.html', user=user)

#用户信息修改
@user.route('/<int:user_id>/userinfoedit', methods=['GET', 'POST'])
def userinfo_edit(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    form = UserInfoForm(obj=user)
    if form.validate_on_submit():
        user.nickname = form.nickname.data
        user.introduction = form.introduction.data
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u"该昵称已经存在", 'warning')
        else:
            flash(u"更新个人信息成功", 'success')
            return redirect(url_for('user.userinfo', user_id=user_id))
    return render_template('user/userInfoEdit.html', form=form)

#用户密码修改
@user.route('/<int:user_id>/passwordedit', methods=['GET', 'POST'])
def password_edit(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    form = PasswordEditForm()
    if form.validate_on_submit():
        if user.check_password(form.currentPassword.data):
            form.update_password(user)
            flash(u"更新密码成功", 'success')
        else:
            flash(u"原密码错误", 'danger')
        return redirect(url_for('user.password_edit', user_id=user_id))
    return render_template('user/passwordEdit.html', form=form)

#############################################
ALLOWED_PDF = set(['pdf'])

def allowed_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PDF

#用户附件简历查看
@user.route('/<int:user_id>/resumeattach', methods=['GET', 'POST'])
def resume_attach(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    if request.method == 'POST':
       if 'file' not in request.files:
           flash(u'没有文件', 'warning')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           flash(u'没有选择的文件', 'warning')
           return redirect(request.url)
       if file and allowed_pdf(file.filename):
           file_type = file.filename.rsplit('.', 1)[1]
           file_name = file.filename.rsplit('.', 1)[0]
           filename = secure_filename('.'.join((file_name,file_type)))
           file_path = os.path.join(current_app.config['USER_RESUME_FOLDER'], current_user.email)
           if not os.path.exists(file_path):
               os.makedirs(file_path, 0o755)
           file.save(os.path.join(file_path, filename))
           #存储用户logo的文件位置
           user.resume_url = '/static/resume/' + current_user.email + '/' + filename
           db.session.add(user)
           db.session.commit()
           flash(u'上传用户pdf简历成功','success')
           return redirect(url_for('user.resume_attach', user_id=user_id))
    return render_template('user/resumeAttach.html', user=user, user_id=user_id)


#####################################

#用户在线简历查看
@user.route('/<int:user_id>/resumeonlinesee', methods=['GET', 'POST'])
def resume_online(user_id):
    return render_template('user/resumeOnline.html', user_id=user_id)

#用户在线简历修改
@user.route('/<int:user_id>/resumeonlineedit')
def resume_online_edit(user_id):
    return redirect(url_for('user.resume_online_jobedit', user_id=user_id))

#用户在线简历工作经验修改
@user.route('/<int:user_id>/resumeonlinejobedit', methods=['GET', 'POST'])
def resume_online_jobedit(user_id):
    user = User.query.get(user_id)
    resume = Resume.query.filter_by(user_id=user_id).first()
    jobexp = resume.job_experience
    form = ResumeOnlineJobEditForm(obj=jobexp)
    if form.validate_on_submit():
        pass
    return render_template('user/resumeOnlineJobEdit.html', user_id=user_id)

#用户的所有简历投递
@user.route('/<int:user_id>/resumedelivery')
def resume_delivery(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Delivery.query.filter_by(user_id=user.id).order_by(Delivery.created_at.desc()).paginate(
        page = page,
        per_page = 10,
        error_out = False
    )
    return render_template('user/resumeDelivery.html', user_id=user_id, pagination=pagination) 

#用户被接受的简历投递
@user.route('/<int:user_id>/resumeaccept')
def resume_accept(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Delivery.query.filter_by(user_id=user.id, status=Delivery.STATUS_ACCEPT).order_by(Delivery.created_at.desc()).paginate(
        page = page,
        per_page = 10,
        error_out = False
    )
    return render_template('user/resumeAccept.html', user_id=user_id, pagination=pagination)

#用户被拒绝的简历投递
@user.route('/<int:user_id>/resumereject')
def resume_reject(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Delivery.query.filter_by(user_id=user.id, status=Delivery.STATUS_REJECT).order_by(Delivery.created_at.desc()).paginate(
        page = page,
        per_page = 10,
        error_out = False
    )
    return render_template('user/resumeReject.html', user_id=user_id, pagination=pagination)

#用户被录取的简历投递
@user.route('/<int:user_id>/resumesuccess')
def resume_success(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Delivery.query.filter_by(user_id=user.id, status=Delivery.STATUS_SUCCESS).order_by(Delivery.created_at.desc()).paginate(
        page = page,
        per_page = 10,
        error_out = False
    )
    return render_template('user/resumeSuccess.html', user_id=user_id, pagination=pagination)



