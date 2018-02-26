from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from flask_login import current_user
from jobplus.models import User, db
from werkzeug.utils import secure_filename
import os
from jobplus.forms import UserInfoForm, PasswordEditForm

user = Blueprint('user', __name__, url_prefix='/user')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user.route('/<int:user_id>/userinfo', methods=['GET', 'POST'])
def userinfo(user_id):
    user = User.query.get_or_404(user_id)
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

@user.route('/<int:user_id>/userinfoedit', methods=['GET', 'POST'])
def userinfo_edit(user_id):
    user = User.query.get_or_404(user_id)
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

@user.route('/<int:user_id>/passwordedit', methods=['GET', 'POST'])
def password_edit(user_id):
    form = PasswordEditForm()
    user = User.query.get_or_404(user_id)
    if form.validate_on_submit():
        if user.check_password(form.currentPassword.data):
            form.update_password(user)
            flash(u"更新密码成功", 'success')
        else:
            flash(u"原密码错误", 'danger')
        return redirect(url_for('user.password_edit', user_id=user_id))
    return render_template('user/passwordEdit.html', form=form)


@user.route('/<int:user_id>/resume', methods=['GET', 'POST'])
def resume(user_id):
    return render_template('user/resume.html')
