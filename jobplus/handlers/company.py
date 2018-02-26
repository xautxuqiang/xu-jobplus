from flask import Blueprint, render_template, request, current_app, redirect, url_for, current_app, flash
from jobplus.models import CompanyInfo, db, User, Job
from werkzeug.utils import secure_filename
import os
from jobplus.forms import CompanyInfoForm, CompanyIntroForm, TeamIntroForm, TagsForm, JobPostForm

company = Blueprint('company', __name__, url_prefix='/company')

#显示所有公司的页面
@company.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = CompanyInfo.query.paginate(
        page = page,
        per_page = current_app.config['COMPANY_PER_PAGE'],
        error_out = False
    )
    return render_template('company/index.html', pagination=pagination)


#显示公司个人的主页
@company.route('/<int:company_id>')
def company_detail(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
    return render_template('company/companyDetail.html', company=company)

#修改公司信息
@company.route('/<int:company_id>/companyedit')
def company_edit(company_id):
    return redirect(url_for('company.company_image_edit', company_id=company_id))

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#修改公司头像
@company.route('/<int:company_id>/imageedit',methods=['GET','POST'])
def company_image_edit(company_id):
    user = CompanyInfo.query.get_or_404(company_id).user
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
def company_info_edit(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
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
def company_tags_edit(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
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
def company_intro_edit(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
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
def team_intro_edit(company_id):
    company = CompanyInfo.query.get_or_404(company_id)
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
def job_post(company_id):
    form = JobPostForm()
    if form.validate_on_submit():
        form.create_job(company_id)
        flash(u"创建该职位成功",'success')
        return redirect(url_for('company.job_posted', company_id=company_id))
    return render_template('job/jobPost.html', form=form, company_id=company_id)

#已发布职位
@company.route('/<int:company_id>/jobposted')
def job_posted(company_id):
    jobs = CompanyInfo.query.get_or_404(company_id).jobs
    page = request.args.get('page', default=1, type=int)
    pagination = jobs.order_by(Job.created_at.desc()).paginate(page=page, per_page=current_app.config['JOB_PER_PAGE'], error_out=False)
    return render_template('job/jobPosted.html', pagination=pagination, company_id=company_id)

#修改已发布职位
@company.route('/<int:company_id>/jobedit/<int:job_id>', methods=['GET','POST'])
def job_edit(company_id, job_id):
    job = Job.query.get_or_404(job_id)
    form = JobPostForm(obj=job)
    if form.validate_on_submit():
        form.create_job(company_id)
        flash(u"修改该职位成功",'success')
        return redirect(url_for('company.job_posted', company_id=company_id))
    return render_template('job/jobEdit.html', form=form, company_id=company_id, job_id=job_id)
