from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from jobplus.models import db, User, CompanyInfo, Job


class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Email()])
    #nickname = StringField(u'昵称', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(6,24)])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError(u'密码错误')

class UserRegisterForm(FlaskForm):
    nickname = StringField(u'昵称', validators=[DataRequired(), Length(1,30)])
    email = StringField(u'邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(6,24)])
    password2 = PasswordField(u'重复密码', validators=[DataRequired(), EqualTo('password', message=u'两次密码必须一致')])
    submit = SubmitField(u'用户注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError(u'该昵称已注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已注册')

    def create_user(self):
        user = User(nickname=self.nickname.data, email=self.email.data, password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user

class CompanyRegisterForm(FlaskForm):
    nickname = StringField(u'用户昵称', validators=[DataRequired(), Length(1,32)])
    company_name = StringField(u'公司名', validators=[DataRequired(), Length(1,64)])
    website = StringField(u'公司站点', validators=[DataRequired(), Length(1,64)])
    email = StringField(u'企业邮箱', validators=[DataRequired(), Email()])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(6,24)])
    password2 = PasswordField(u'重复密码', validators=[DataRequired(), EqualTo('password', message=u'两次密码必须一致')])
    submit = SubmitField(u'企业注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError(u'该用户昵称已注册')

    def validate_company_name(self, field):
        if CompanyInfo.query.filter_by(company_name=field.data).first():
            raise ValidationError(u'该公司名已注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该企业邮箱已注册')

    def validate_website(self, field):
        if CompanyInfo.query.filter_by(website=field.data).first():
            raise ValidationError(u'该站点已注册')

    def create_user(self):
        user = User(nickname=self.nickname.data, email=self.email.data, password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user

class UserInfoForm(FlaskForm):
    nickname = StringField(u'昵称', validators=[DataRequired(), Length(1,32)]) 
    introduction = TextAreaField(u'一句话简介', validators=[Length(0,256)])
    submit = SubmitField(u'更新')

    def update_userinfo(self, user):
        user.nickname = self.nickname.data
        user.introduction = self.introduction.data
        db.session.add(user)
        db.session.commit()
        return user

class PasswordEditForm(FlaskForm):
    currentPassword = PasswordField(u'原密码', validators=[DataRequired(), Length(6,24)])
    newPassword = PasswordField(u'新密码', validators=[DataRequired(), Length(6,24)])
    newPassword2 = PasswordField(u'重复密码', validators=[DataRequired(), EqualTo('newPassword', message=u'两次密码必须一致')])
    submit = SubmitField(u"确定")
    
    #判断原密码是否正确
    def password_judge(self, user):
        if not user.check_password(self.currentPassword.data):
            raise ValidationError(u"原密码错误")

    def update_password(self, user):
        user.password = self.newPassword.data
        db.session.add(user)
        db.session.commit()
        return user

#基本信息
class CompanyInfoForm(FlaskForm):
    company_name = StringField(u'企业名称', validators=[DataRequired(), Length(1,64)])
    website = StringField(u'公司网站', validators=[DataRequired(), Length(1,64)])
    description = StringField(u'一句话描述', validators=[DataRequired(), Length(1,128)]) 
    field = SelectField(u'公司领域', choices = [
               (u'移动互联网', u'移动互联网'),
               (u'电子商务', u'电子商务'),
               (u'金融', u'金融'),
               (u'企业服务', u'企业服务'),
               (u'社交网络', u'社交网络')
            ])
    finance_stage = SelectField(u'融资阶段', choices = [
               (u'未融资', u'未融资'),
               (u'天使轮', u'天使轮'),
               (u'A轮', u'A轮'),
               (u'B轮', u'B轮'),
               (u'C轮', u'C轮'),
               (u'D轮及以上', u'D轮及以上'),
               (u'上市公司', u'上市公司'),
               (u'不需要融资', u'不需要融资')
    ]) 
    scale = SelectField(u'公司规模', choices = [
               (u'15-50人', u'15-50人'),
               (u'50-150人', u'50-150人'),
               (u'150-500人', u'150-500人'),
               (u'500-2000人', u'500-2000人')
            ]) 
    city = SelectField(u'所在城市', choices = [
               (u'北京', u'北京'),
               (u'上海', u'上海'),
               (u'深圳', u'深圳'),
               (u'广州', u'广州'),
               (u'杭州', u'杭州'),
               (u'成都', u'成都'),
               (u'南京', u'南京'),
               (u'武汉', u'武汉'),
               (u'西安', u'西安'),
               (u'厦门', u'厦门')
        ]) 
    submit = SubmitField(u'确定')


#福利标签
class TagsForm(FlaskForm):
    tags = StringField(u'福利标签', validators=[Length(0,512)])
    submit = SubmitField(u'确定')

#公司介绍表单
class CompanyIntroForm(FlaskForm):
    company_intro = TextAreaField(u'公司介绍', validators=[Length(0,1500)])
    submit = SubmitField(u'确定')

#团队介绍表单
class TeamIntroForm(FlaskForm):
    team_intro = TextAreaField(u'团队介绍', validators=[Length(0,1500)])
    submit = SubmitField(u'确定')

#职位创建表单
class JobPostForm(FlaskForm):
    job_name = StringField(u'职位名称', validators=[DataRequired(), Length(1,32)])
    salary_low = StringField(u'薪水下限', validators=[DataRequired()])
    salary_high = StringField(u'薪水上限', validators=[DataRequired()])
    experience_requirement = SelectField(u'工作经验', choices=[
            (u'应届毕业生',u'应届毕业生'),
            (u'1年以内',u'1年以内'),
            (u'1-3年',u'1-3年'),
            (u'3-5年',u'3-5年'),
            (u'5年以上',u'5年以上'),
            (u'不要求',u'不要求')     
    ])
    degree_requirement = SelectField(u'学历要求', choices=[
            (u'大专',u'大专'),
            (u'本科',u'本科'),
            (u'硕士',u'硕士'),
            (u'博士',u'博士'),
            (u'不要求',u'不要求')
    ])
    work_location_city = SelectField(u'工作所在城市', choices = [
               (u'北京', u'北京'),
               (u'上海', u'上海'),
               (u'深圳', u'深圳'),
               (u'广州', u'广州'),
               (u'杭州', u'杭州'),
               (u'成都', u'成都'),
               (u'南京', u'南京'),
               (u'武汉', u'武汉'),
               (u'西安', u'西安'),
               (u'厦门', u'厦门')
        ])
    work_location_district = StringField(u'所属区域', validators=[DataRequired(), Length(1,32)])
    work_location_address = StringField(u'具体地址', validators=[DataRequired(), Length(1,128)])
    tags = StringField(u'职位标签', validators=[Length(0,256)])
    is_fulltime = SelectField(u'是否全职', coerce=int, choices=[
            (1, u'全职'),
            (0, u'实习')    
    ])
    job_description = TextAreaField(u'职位描述')
    job_requirement = TextAreaField(u'职位要求')
    submit = SubmitField(u'确定')

    def create_job(self, company_id):
        job = Job(job_name=self.job_name.data, salary_low=self.salary_low.data, salary_high=self.salary_high.data, experience_requirement=self.experience_requirement.data, degree_requirement=self.degree_requirement.data, work_location_city=self.work_location_city.data, work_location_district=self.work_location_district.data, work_location_address=self.work_location_address.data, tags=self.tags.data, is_fulltime=self.is_fulltime.data, job_description=self.job_description.data, job_requirement=self.job_requirement.data, company_id=company_id)
        db.session.add(job)
        db.session.commit()
        return job 
