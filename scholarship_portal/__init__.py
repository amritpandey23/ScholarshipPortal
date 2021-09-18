import json
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

with open("config.json") as f:
    _config = json.load(f)

app = Flask(__name__)

app.config["SECRET_KEY"] = _config["app_secret"]
app.config["SQLALCHEMY_DATABASE_URI"] = _config["db_uri"]


bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'student_login'
login_manager.login_message_category = 'info'

import scholarship_portal.routes