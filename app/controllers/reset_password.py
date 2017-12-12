
from flask import render_template, \
    Blueprint, \
    request, \
    jsonify
from werkzeug import generate_password_hash, check_password_hash
from app import app
from app.models import User
from app.database.utils import filterSpecificObject, \
    commitChanges

from app.utils.mail import mail
from flask_mail import Message
import logging

logger = logging.getLogger(app.config['LOG_FILE'])
reset_password = Blueprint('reset_password',
                   __name__,
                   template_folder='templates')

@reset_password.route('/resetPassword', methods=['POST'])
def resetPassword():
    """
    Handling reset password request from the user, generating an auth token
    which expires in 30 minutes. sending an email to the user which including
    url link to reset is password
    :return:
    """
    try:
        res = {'error':'Failed to restore password'}
        user = filterSpecificObject(User, username=request.form['email'])
        if user:
            token = user.generate_auth_token(1800)
            with mail.connect() as conn:
                subject = 'Password reset'
                message = """Hello %s,
You ask to reset your password
please click %s/%s
in case it is not you, ignore this mail.""" % (user.name,request.base_url,token)
                msg = Message(subject=subject,
                              sender=app.config['MAIL_USERNAME'],
                              recipients=[user.username],
                              body=message)
                conn.send(msg)
            res = {'title': 'Please confirm password reset',
                   'message': 'Mail including password reset link sent to your mailbox'}
        else:
            res = {'error':'Account is not exist'}
    except Exception as e:
        logger.warning(e)
    finally:
        return jsonify(res)

@reset_password.route('/resetPassword/<token>')
def authToken(token):
    """
    Redirecting to reset password page if token is valid
    :param token: auth token
    :return: json response
    """
    user = User.verify_auth_token(token)
    if not user:
        return render_template('error.html', error='Unauthorized Access')
    return render_template('reset_password.html', token=token)

@reset_password.route('/updatePassword',methods=['POST'])
def updatePassword():
    """
    Updating user password
    :return: json response
    """
    user = User.verify_auth_token(request.values.get('token', None))
    if not user:
        return jsonify({'error':'Failed to update password'})
    hashed_password = generate_password_hash(request.values.get('password', None))
    user.password = hashed_password
    commitChanges()
    return jsonify({'message':'Password updated','title':'Update'})

@reset_password.route('/forgotPassword')
def forgotPassword():
    return render_template('forgot_password.html')