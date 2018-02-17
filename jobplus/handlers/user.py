from flask import Blueprint, render_template

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/')
def index():
    return render_template('user/index.html')
