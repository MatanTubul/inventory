from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
app = Flask(__name__)
app.secret_key = 'r?4#/FUKr6u;Vh<s|d1:6-NPg^Rhy]'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:edco123@localhost/wintventory'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from controllers.routes import routes
app.register_blueprint(routes)
