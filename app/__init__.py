from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_pymongo import PyMongo


app = Flask(__name__)

app.secret_key = 'r?4#/FUKr6u;Vh<s|d1:6-NPg^Rhy]'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:edco123@localhost/wintventory'
# app.config['SQLALCHEMY_ECHO'] = True
app.config['LOG_FILE'] = 'wintventory.log'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mongo = PyMongo(app)
from controllers.routes import routes
app.register_blueprint(routes)
