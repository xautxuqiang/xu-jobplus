from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

user_job = db.Table(
    'user_job',
     db.Column('user.id', db.Integer, db.ForeignKey('user.id',ondelete='CASCADE')),
     db.Column('job_id', db.Integer, db.ForeignKey('job.id',ondelete='CASCADE'))
)

#用户表
class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10 
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    #头像 -> 静态文件实现
    logo = db.Column(db.String(256), default="/static/user/default/default.png")
    #昵称
    nickname = db.Column(db.String(32), nullable=False, unique=True)
    #邮箱
    email = db.Column(db.String(64), nullable=False, unique=True)
    #密码
    _password = db.Column('password', db.String(256), nullable=False)
    #个人介绍
    introduction = db.Column(db.String(256), default="")
    #职位
    job = db.Column(db.String(64))
    #角色
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    #对应公司
    detail = db.relationship('CompanyInfo', uselist=False)

    is_disable = db.Column(db.Boolean, default=False)

    #求职者和工作多对多关系
    collect_jobs = db.relationship('Job', secondary=user_job, lazy='subquery', backref=db.backref('users', lazy=True))
    #求职者和简历一对一关系
    resume = db.relationship('Resume', uselist=False)
    #pdf简历存储
    resume_url = db.Column(db.String(256), default='')
    #选择在线简历还是附件简历,1为附件,0为在线
    resume_mode = db.Column(db.Integer, default=1)

    #密码属性
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    #角色属性
    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def __repr__(self):
        return '<User {}>'.format(self.email)

class Resume(Base):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True)
    #简历和求职者一对一关系
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)
    job_experience = db.relationship('JobExperience')
    edu_experience = db.relationship('EduExperience')
    project_experience = db.relationship('ProjectExperience')

class Experience(Base):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    begin_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    description = db.Column(db.Text)

#工作经验
class JobExperience(Experience):
    __tablename__ = 'job_experience'

    #公司，职位
    company = db.Column(db.String(32), nullable=False, default='')
    company_job = db.Column(db.String(32), nullable=False, default='')
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

#教育经验
class EduExperience(Experience):
    __tablename__ = 'edu_experience'

    school = db.Column(db.String(32), nullable=False, default='')
    #专业
    specialty = db.Column(db.String(32), nullable=False, default='')
    degree = db.Column(db.String(16), default='')
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

#项目经验
class ProjectExperience(Experience):
    __tablename__ = 'project_experience'

    name = db.Column(db.String(32), nullable=False, default='')
    #项目中的角色
    role = db.Column(db.String(32), default='')
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)


#职位表
class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    #职位名称
    job_name = db.Column(db.String(32), nullable=False)
    #薪水下限
    salary_low = db.Column(db.SmallInteger, nullable=False)
    #薪水上限
    salary_high = db.Column(db.SmallInteger, nullable=False)
    #工作经验要求
    experience_requirement = db.Column(db.String(32), default='') 
    #学历要求 
    degree_requirement = db.Column(db.String(32), default='')
    #工作地址之城市
    work_location_city = db.Column(db.String(32), default='')
    #工作地址之区域
    work_location_district = db.Column(db.String(32), default='')
    #工作地址之具体位置
    work_location_address = db.Column(db.String(128), default='')
    #职位描述
    job_description = db.Column(db.Text, default='')
    #职位要求
    job_requirement = db.Column(db.Text, default='')
    #职位标签,逗号隔开,最多10个
    tags = db.Column(db.String(256), default='')
    #是否全职
    is_fulltime = db.Column(db.Boolean, default=True)
    #是否在招聘
    is_open = db.Column(db.Boolean, default=True)
    #查看次数
    views_count = db.Column(db.Integer, default=0)

    #job外键->公司
    company_id = db.Column(db.Integer, db.ForeignKey('company_info.id'), nullable=False)

    @property
    def tag_list(self):
        return self.tags.split(',')

    def __repr__(self):
        return '<Job {}>'.format(self.job_name)

#企业表
class CompanyInfo(Base):
    __tablename__ = 'company_info'

    id = db.Column(db.Integer, primary_key=True)
    #企业logo使用static文件实现，直接链接图片
    logo = db.Column(db.String(256), default="/static/company/default.png")
    #企业名称
    company_name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    #企业网站
    website = db.Column(db.String(64), nullable=False, index=True, unique=True)
    #公司城市
    city = db.Column(db.String(128), default='')
    #一句话描述
    description = db.Column(db.String(128), default=u'一句话让别人了解你')
    #公司详细介绍
    company_intro = db.Column(db.Text, default='')
    #团队详细介绍
    team_intro = db.Column(db.Text, default='')
    #公司福利标签,标签多.最大10个
    tags = db.Column(db.String(512), default='')
    #公司领域,至多两个标签
    field = db.Column(db.String(128), default='')
    #融资进度
    finance_stage = db.Column(db.String(128), default='')
    #公司规模（人数）
    scale = db.Column(db.String(32), default='')    
    #企业对应的企业用户
    user = db.relationship('User', uselist=False, backref=db.backref('company_info', uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    #企业对应的job-一对多
    jobs = db.relationship('Job', backref="company_info", lazy="dynamic")

    #查看次数
    views_count = db.Column(db.Integer, default=0)

    @property
    def tag_list(self):
        return self.tags.split(',')

    def __repr__(self):
        return '<Comapny {}>'.format(self.company_name)

#投递表
class Delivery(Base):
    __tablename__ = 'delivery'

    #待接收
    STATUS_WAITING = 1
    #被拒绝
    STATUS_REJECT = 2
    #已接收,待面试
    STATUS_ACCEPT = 3
    #录取
    STATUS_SUCCESS = 4

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    company_id = db.Column(db.Integer, db.ForeignKey('company_info.id', ondelete='SET NULL'))
    status = db.Column(db.SmallInteger, default=STATUS_WAITING)
    response = db.Column(db.String(256))

    @property
    def user(self):
        return User.query.get(self.user_id)

    @property
    def job(self):
        return Job.query.get(self.job_id)

    @property
    def company(self):
        return CompanyInfo.query.get(self.company_id)

