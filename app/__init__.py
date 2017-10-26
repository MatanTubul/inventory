from flask import Flask
app = Flask(__name__)
app.secret_key = 'r?4#/FUKr6u;Vh<s|d1:6-NPg^Rhy]'
from controllers.routes import routes
app.register_blueprint(routes)