#基本配置
class BaseConfig(object):
    SECRET_KEY = 'project jobplus'

#开发配置
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:xqxq1994@localhost:3306/jobplus?charset=utf8'
    #跟踪修改对象，发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #用户图片存储位置
    USER_LOGO_FOLDER = '/home/xu/xu-jobplus/jobplus/static/user' 
    #公司图片存储位置
    COMPANY_LOGO_FOLDER = '/home/xu/xu-jobplus/jobplus/static/company'
    #每页公司的数目
    COMPANY_PER_PAGE = 16
    #每页工作的条目数
    JOB_PER_PAGE = 20

#产品配置
class ProductionConfig(BaseConfig):
    pass

#测试配置
class TestingConfig(BaseConfig):
    Testing = True


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
