from flask import render_template, \
    Blueprint, \
    request, \
    session, \
    json
from werkzeug import generate_password_hash, check_password_hash
from app import app
from app.models import User
from app.database.utils import filterSpecificObject, \
    addObject, \
    getUsersList

import logging

logger = logging.getLogger(app.config['LOG_FILE'])
sign_up = Blueprint('sign_up',
                   __name__,
                   template_folder='templates')

@sign_up.route('/showSignUp')
def showSignUp():
    if session.get('user'):
        return render_template('signup.html', users=getUsersList(User),
                               role=session.get('role'),
                               user=session.get('user'))
    else:
        return render_template('error.html', error='Unauthorized Access')

@sign_up.route('/signUp', methods=['POST'])
def signUp():
    """
    # read signUp values from UI
    :return:
    """
    res =""
    try:
        name = request.form['inputName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        role = request.form['inputUserRule']
        hashed_password = generate_password_hash(password)
        # validate the received values
        if (filterSpecificObject(User, username=email)):
            res = {'error': 'User already exists'}
        else:
            u = User(email,
                     hashed_password,
                     name,
                     role)
            addObject(u)
            res = {'message': 'User created successfully !'}
    except Exception as e:
        logger.warning(e)
        res = {'error': "Failed to create user"}
    finally:
        return json.dumps(res)
