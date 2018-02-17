from flask import Flask
from jobplus.config import configs
from jobplus.models import db
from jobplus.handlers import front, company, user, admin, job
from flask_migrate import Migrate

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    #注册扩展
    register_extensions(app)
    #注册蓝图
    register_blueprints(app)

    return app

#注册狂扩展
def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    
#注册蓝图
def register_blueprints(app):
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(company)
    app.register_blueprint(user)
    app.register_blueprint(job)

