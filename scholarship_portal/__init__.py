import json
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

with open("config.json") as f:
    _config = json.load(f)

app = Flask(__name__)

app.config["SECRET_KEY"] = _config["app_secret"]
app.config["SQLALCHEMY_DATABASE_URI"] = _config["db_uri"]


bcrypt = Bcrypt(app)

db = SQLAlchemy(app)

@app.route("/", methods=["GET", "POST"])
def home():
    return "Hello World"