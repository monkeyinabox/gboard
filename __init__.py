from flask import Flask
from flask_login import LoginManager

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    mail.init_app(app)
    return app


app = create_app()
app.app_context().push()

# INIT EXTENSIONS
# flask-bcrypt
flask_bcrypt = Bcrypt(app)

from .models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()

# LOAD VIEWS
from gboard import views