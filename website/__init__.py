from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('website.config.DevelopmentConfig')

mail = Mail(app)
db = SQLAlchemy(app)

# Blueprints

from website.blueprints.auth import auth
from website.blueprints.views import views
from website.blueprints.settings import settings

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(settings, url_prefix='/')

# login manager

from .models import User

if not path.exists('instance/financeapp.db'):
    with app.app_context():
        db.create_all()
        print('database created')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
