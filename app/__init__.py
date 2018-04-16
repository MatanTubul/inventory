from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_pymongo import PyMongo


app = Flask(__name__)

app.secret_key = 'r?4#/FUKr6u;Vh<s|d1:6-NPg^Rhy]'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:edco123@localhost/wintventory'
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LOG_FILE'] = 'wintventory.log'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mongo = PyMongo(app)
from database.utils import dbSetup

@app.before_first_request
def setup():
    dbSetup()

from controllers.reports import report
from controllers.action_history import history
from controllers.users import users
from controllers.devices import devices
from controllers.reset_password import reset_password
from controllers.login import login
from controllers.sign_up import sign_up
from controllers.accounts import account

app.register_blueprint(report)
app.register_blueprint(history)
app.register_blueprint(users)
app.register_blueprint(devices)
app.register_blueprint(reset_password)
app.register_blueprint(login)
app.register_blueprint(sign_up)
app.register_blueprint(account)

