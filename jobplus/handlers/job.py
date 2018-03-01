from flask import Blueprint, render_template, request, url_for, current_app, redirect, flash
from jobplus.models import db, Job, Delivery
from flask_login import current_user

job = Blueprint('job', __name__, url_prefix='/job')

#按时间显示所有的工作列表
@job.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.order_by(Job.created_at.desc()).paginate(
        page = page,
        per_page = current_app.config['JOB_PER_PAGE'],
        error_out = False 
    )
    return render_template('job/index.html', pagination=pagination)

#显示工作详细页面
@job.route('/<int:job_id>/jobdetail', methods=['GET','POST'])
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    job.views_count += 1
    try:
        db.session.add(job)
        db.session.commit()
    except:
        db.session.rollback()
        flash(u'增加职位浏览次数失败', 'warning')
    has_been_delivered = False
    #判断该职位用户是否已经投递
    user = current_user
    #and判断，第一项为假。则直接跳过
    if not user.is_anonymous and job in user.collect_jobs:
        has_been_delivered = True
    #方法为POST时   
    if request.method == 'POST':
        user.resume_mode = request.form.get('resumeRadio')
        user.collect_jobs.append(job)
        d = Delivery(job_id=job.id, user_id=user.id, company_id=job.company_id)
        try:
            db.session.add(user)
            db.session.add(d)
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'投递失败','warning')
        else:
            flash(u'投递成功','success')
            return redirect(url_for('job.job_detail', job_id=job_id))
    return render_template('job/jobDetail.html',has_been_delivered=has_been_delivered, job=job)

