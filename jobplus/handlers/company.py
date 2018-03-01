from flask import Blueprint, render_template, request, current_app, redirect, url_for, current_app, flash, abort
from jobplus.models import CompanyInfo, db, User, Job, Delivery
from werkzeug.utils import secure_filename
import os
from jobplus.forms import CompanyInfoForm, CompanyIntroForm, TeamIntroForm, TagsForm, JobPostForm
from flask_login import current_user, login_required

company = Blueprint('company', __name__, url_prefix='/company')

#显示所有公司的页面
@company.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = CompanyInfo.query.order_by(CompanyInfo.created_at.desc()).paginate(
        page = page,
        per_page = current_app.config['COMPANY_PER_PAGE'],
        error_out = False
    )
    return render_template('company/index.html', pagination=pagination)


#显示公司个人的主页
@company.route('/<int:company_id>')
def company_detail(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    company.views_count += 1
    try:
        db.session.add(company)
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'增加公司被查看次数失败','warning')
    return render_template('company/companyDetail.html', company=company)

#公司在招职位
@company.route('/<int:company_id>/jobavaliable')
def company_job_avaliable(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(company_id=company_id).paginate(
            page = page,
            per_page = 10,
            error_out = False
    )
    return render_template('company/jobAvaliable.html', company=company, pagination=pagination)

#修改公司信息
@company.route('/<int:company_id>/companyedit')
def company_edit(company_id):
    return redirect(url_for('company.company_image_edit', company_id=company_id))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#修改公司头像
@company.route('/<int:company_id>/imageedit',methods=['GET','POST'])
@login_required
def company_image_edit(company_id):
    user = CompanyInfo.query.get_or_404(company_id).user
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
           file_path = os.path.join(current_app.config['COMPANY_LOGO_FOLDER'], user.email)
           if not os.path.exists(file_path):
               os.makedirs(file_path, 0o755)
           file.save(os.path.join(file_path, filename))
           #存储公司logo的文件位置
           user.detail.logo = '/static/company/' + user.email + '/' + filename
           try:
               db.session.add(user)
               db.session.commit()
           except:
               db.session.rollback()
               flash(u'修改logo失败','warning')
               return redirect(url_for('company.company_image_edit', company_id=company_id))
           else:
               flash(u'修改logo成功','success')
               return redirect(url_for('company.company_detail', company_id=user.detail.id))
    return render_template('company/companyImageEdit.html', company_id=company_id)

#修改公司基本信息
@company.route('/<int:company_id>/basicinfoedit', methods=['GET','POST'])
@login_required
def company_info_edit(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    if current_user.is_anonymous or current_user.id != company.user.id:
        abort(404)
    form = CompanyInfoForm(obj=company)
    if form.is_submitted():
        company.company_name = form.company_name.data
        company.website = form.website.data
        try:
            db.session.add(company)
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'公司名或站点已被注册', 'warning')
            return redirect(url_for('company.company_info_edit', company_id=company_id))
        company.description = form.description.data
        company.field = form.field.data
        company.finance_stage = form.finance_stage.data
        company.city = form.city.data
        company.scale = form.scale.data
        db.session.add(company)
        db.session.commit()
        flash(u'修改公司基本信息成功','success')
        return redirect(url_for('company.company_detail', company_id=company_id))
    return render_template('company/companyInfoEdit.html', company_id=company_id, form=form)

#公司福利标签
@company.route('/<int:company_id>/tagsedit', methods=['GET','POST'])
@login_required
def company_tags_edit(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    if current_user.is_anonymous or current_user.id != company.user.id:
        abort(404)
    form = TagsForm(obj=company)
    if form.validate_on_submit():
        company.tags = form.tags.data
        try:
            db.session.add(company)
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'修改公司福利标签失败', 'warning')
            return redirect(url_for('company.company_tags_edit', company_id=company_id))
        flash(u'修改用户福利标签成功', 'success')
        return redirect(url_for('company.company_detail', company_id=company_id))
    return render_template('company/companyTagsEdit.html', form=form, company_id=company_id)

#修改公司介绍
@company.route('/<int:company_id>/comintroedit', methods=['GET','POST'])
@login_required
def company_intro_edit(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    if current_user.is_anonymous or current_user.id != company.user.id:
        abort(404)
    form = CompanyIntroForm(obj=company)
    if form.validate_on_submit():
        company.company_intro = form.company_intro.data
        try:
            db.session.add(company)
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'修改公司介绍失败','warning')
            return redirect(url_for('company.company_intro_edit', company_id=company_id))
        else:
            flash(u'修改公司介绍成功', 'success')
            return redirect(url_for('company.company_detail', company_id=company_id))
    return render_template('company/companyIntroEdit.html',form=form, company_id=company_id)

#修改团队介绍
@company.route('/<int:company_id>/teamintroedit', methods=['GET','POST'])
@login_required
def team_intro_edit(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    if current_user.is_anonymous or current_user.id != company.user.id:
        abort(404)
    form = TeamIntroForm(obj=company)
    if form.validate_on_submit():
        company.team_intro = form.team_intro.data
        try:
            db.session.add(company)
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'修改团队介绍失败','warning')
            return redirect(url_for('company.team_intro_edit', company_id=company_id))
        else:
            flash(u'修改团队介绍成功', 'success')
            return redirect(url_for('company.company_detail', company_id=company_id))
    return render_template('company/teamIntroEdit.html', form=form, company_id=company_id)


#发布职位
@company.route('/<int:company_id>/jobpost', methods=['GET','POST'])
@login_required
def job_post(company_id):
    user = CompanyInfo.query.get_or_404(company_id).user
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    form = JobPostForm()
    if form.validate_on_submit():
        form.create_job(company_id)
        flash(u"创建该职位成功",'success')
        return redirect(url_for('company.job_posted', company_id=company_id))
    return render_template('job/jobPost.html', form=form, company_id=company_id)

#已发布职位
@company.route('/<int:company_id>/jobposted')
@login_required
def job_posted(company_id):
    jobs = CompanyInfo.query.get_or_404(company_id).jobs
    page = request.args.get('page', default=1, type=int)
    pagination = jobs.order_by(Job.created_at.desc()).paginate(page=page, per_page=current_app.config['JOB_PER_PAGE'], error_out=False)
    return render_template('job/jobPosted.html', pagination=pagination, company_id=company_id)

#修改已发布职位
@company.route('/<int:company_id>/jobedit/<int:job_id>', methods=['GET','POST'])
@login_required
def job_edit(company_id, job_id):
    user = CompanyInfo.query.get_or_404(company_id).user
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    job = Job.query.get_or_404(job_id)
    form = JobPostForm(obj=job)
    if form.validate_on_submit():
        form.create_job(company_id)
        flash(u"修改该职位成功",'success')
        return redirect(url_for('company.job_posted', company_id=company_id))
    return render_template('job/jobEdit.html', form=form, company_id=company_id, job_id=job_id)

#删除已发布职位
@company.route('/<int:company_id>/jobdelete/<int:job_id>', methods=['GET', 'POST'])
@login_required
def job_delete(company_id, job_id):
    user = CompanyInfo.query.get_or_404(company_id).user
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    job = Job.query.get_or_404(job_id)
    #删除job的同时也删除掉这个职位对应的简历投递
    job_d = Delivery.query.filter_by(job_id=job.id).all()
    for d in job_d:
        db.session.delete(d)
        db.session.commit()
    #删除相关职位
    try:
        db.session.delete(job)
        db.session.commit()
    except:
        db.rollback()
        flash(u'删除该职位失败', 'warning')
        return redirect(url_for('company.job_delete', company_id=company_id, job_id=job_id))
    else:
        flash(u'删除该职位成功', 'success')
        return redirect(url_for('company.job_posted', company_id=company_id))
        

#公司接收到的所有简历投递
@company.route('/<int:company_id>/companyresume', methods=['GET', 'POST'])
@login_required
def company_resume(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    if current_user.is_anonymous or current_user.id != company.user.id:
        abort(404)
    page = request.args.get('page', default=1, type=int)
    pagination = Delivery.query.filter_by(company_id=company_id).order_by(Delivery.created_at.desc()).paginate(
        page = page,
        per_page = 10,
        error_out = False
    )
    return render_template('company/companyResume.html', company_id=company_id, pagination=pagination) 

#公司拒绝的简历投递
@company.route('/<int:company_id>/companyresumereject', methods=['GET', 'POST'])
@login_required
def company_resume_reject(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    if current_user.is_anonymous or current_user.id != company.user.id:
        abort(404)
    page = request.args.get('page', default=1, type=int)
    pagination = Delivery.query.filter_by(company_id=company_id, status=Delivery.STATUS_REJECT).order_by(Delivery.created_at.desc()).paginate(
        page = page,
        per_page = 10,
        error_out = False
    )
    return render_template('company/companyResumeReject.html', company_id=company_id, pagination=pagination)

#拒绝某简历
@company.route('/<int:company_id>/job/<int:job_id>/user/<int:user_id>/reject', methods=['GET', 'POST'])
@login_required
def company_reject_resume(company_id, job_id, user_id):
    user = CompanyInfo.query.get_or_404(company_id).user
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    d = Delivery.query.filter_by(company_id=company_id, job_id=job_id, user_id=user_id).first_or_404()    
    d.status = Delivery.STATUS_REJECT
    try:
        db.session.add(d)
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'拒绝操作失败', 'warning')
        return redirect(url_for('company.company_reject_resume', company_id=company_id, job_id=job_id, user_id=user_id))
    else:
        flash(u'拒绝操作成功', 'success')
        return redirect(url_for('company.company_resume_reject', company_id=company_id))

#公司确认接收的简历投递
@company.route('/<int:company_id>/companyresumeaccept', methods=['GET', 'POST'])
@login_required
def company_resume_accept(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Delivery.query.filter_by(company_id=company_id, status=Delivery.STATUS_ACCEPT).order_by(Delivery.created_at.desc()).paginate(
        page = page,
        per_page = 10,
        error_out = False
    )
    return render_template('company/companyResumeAccept.html', company_id=company_id, pagination=pagination)

#接收某简历
@company.route('/<int:company_id>/job/<int:job_id>/user/<int:user_id>/accept', methods=['GET', 'POST'])
def company_accept_resume(company_id, job_id, user_id):
    user = CompanyInfo.query.get_or_404(company_id).user
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    d = Delivery.query.filter_by(company_id=company_id, job_id=job_id, user_id=user_id).first_or_404()
    d.status = Delivery.STATUS_ACCEPT
    try:
        db.session.add(d)
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'接收操作失败', 'warning')
        return redirect(url_for('company.company_accept_resume', company_id=company_id, job_id=job_id, user_id=user_id))
    else:
        flash(u'接收操作成功', 'success')
        return redirect(url_for('company.company_resume_accept', company_id=company_id))

#简历成功状态
@company.route('/<int:company_id>/companyresumesuccess', methods=['GET', 'POST'])
@login_required
def company_resume_success(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    page = request.args.get('page', default=1, type=int)
    pagination = Delivery.query.filter_by(company_id=company_id, status=Delivery.STATUS_SUCCESS).order_by(Delivery.created_at.desc()).paginate(
        page = page,
        per_page = 10,
        error_out = False
    )
    return render_template('company/companyResumeSuccess.html', company_id=company_id, pagination=pagination)

#录取简历
#接收某简历
@company.route('/<int:company_id>/job/<int:job_id>/user/<int:user_id>/success', methods=['GET', 'POST'])
def company_success_resume(company_id, job_id, user_id):
    user = CompanyInfo.query.get_or_404(company_id).user
    if current_user.is_anonymous or current_user.id != user.id:
        abort(404)
    d = Delivery.query.filter_by(company_id=company_id, job_id=job_id, user_id=user_id).first_or_404()
    d.status = Delivery.STATUS_SUCCESS
    try:
        db.session.add(d)
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'录取操作失败', 'warning')
        return redirect(url_for('company.company_success_resume', company_id=company_id, job_id=job_id, user_id=user_id))
    else:
        flash(u'录取操作成功', 'success')
        return redirect(url_for('company.company_resume_success', company_id=company_id))
