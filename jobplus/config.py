#基本配置
class BaseConfig(object):
    SECERT_KEY = 'project jobplus'

#开发配置
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:xqxq1994@localhost:3306/jobplus?charset=utf8'
    #跟踪修改对象，发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
