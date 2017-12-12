
from flask import Blueprint, \
    request, \
    redirect,\
    session, \
    json, jsonify
from flask import render_template
from werkzeug import generate_password_hash, check_password_hash
from app import app
from app.models import User
from app.database.utils import filterSpecificObject
import logging


logger = logging.getLogger(app.config['LOG_FILE'])
login = Blueprint('login',
                   __name__,
                   template_folder='templates')

@login.route('/showSignin')
def showSignin():
    """
    Loading sign in page
    :return: sign in template
    """
    return render_template('signin.html')

@login.route('/validateLogin', methods=['POST'])
def validateLogin():
    """
    # Validate user login params
    :return:
    """
    try:
        username = request.form['inputEmail']
        password = request.form['inputPassword']
        # cursor.callproc('loginValidate',(username,))
        user = filterSpecificObject(User, username=username, isDeleted=0)

        if user:
            if check_password_hash(str(user.password), password):
                session['user'] = user.name
                session['userName'] = user.username
                session['role'] = user.role
                return json.dumps({'url':'/userHome'})
            else:
                return json.dumps({'error':'Wrong Email address or Password.'})
        else:
            return json.dumps({'error':'Wrong Email address or Password.'})
    except Exception as e:
        logger.warning(e)
        return jsonify({'error':'validateLogin failed'})

@login.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')