from flask import Blueprint, render_template, request, url_for, current_app
from jobplus.models import db, Job

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
@job.route('/<int:job_id>/jobdetail')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/jobDetail.html', job=job)

