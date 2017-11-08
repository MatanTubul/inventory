from datetime import datetime
from flask import render_template, \
    Blueprint, \
    request, \
    redirect,\
    session, \
    json, jsonify
from werkzeug import generate_password_hash, check_password_hash
from app import app
from app.models import User, Device, History
from app.database.utils import dbSetup, \
    getDevicesList, \
    filterSpecificObject, \
    setObjectIsDeleted, \
    commitChanges, \
    addObject, \
    selectObject, \
    getUsersList, \
    getEventsHistory
from app.utils.mail import mail
from flask_mail import Message
import logging
logger = logging.getLogger(app.config['LOG_FILE'])
routes = Blueprint('controllers',
                   __name__,
                   template_folder='templates')
@app.before_first_request
def setup():
    dbSetup()

@routes.route("/")
def main():
    # if session is active redirect to home page
    if session.get('user'):
        # cursor.callproc('get_devices_list')
        devicesList = getDevicesList(Device)
        return render_template('userHome.html', devices = devicesList,
                               role=session.get('role'),
                               user=session.get('user'),
                               username=session.get('userName')
                               )

    return render_template('signin.html')

@routes.route('/userHome', methods=['GET','POST'])
def userHome():
    """
    Loading app home page after user login successfully,
     in case login failed user redirect to error page.
    :return: template
    """

    if session.get('user'):
        # cursor.callproc('get_devices_list')
        devicesList = getDevicesList(Device)
        return render_template('userHome.html',
                               devices = devicesList,
                               role=session.get('role'),
                               user=session.get('user'),
                               username=session.get('userName')
                               )
    else:
        return render_template('error.html', error='Unauthorized Access')

@routes.route('/deleteDevice', methods=['POST'])
def deleteDevice():
    """
    Handling delete device record request, in case of succesful,
    home page got render, otherwise popup message appear
    :return: response message
    """
    res = ""
    try:
        device = filterSpecificObject(Device,
                                      macAddress=request.values.get('mac_address', None))
        setObjectIsDeleted(device)
        res = {'message': 'Device deleted successfully'}
    except Exception as e:
        logger.warning(e)
        res = {'error': 'Delete device failed'}
    finally:
        return jsonify(res)

@routes.route('/showSignUp')
def showSignUp():
    if session.get('user'):
        return render_template('signup.html', users=getUsersList(User),
                               role=session.get('role'),
                               user=session.get('user'))
    else:
        return render_template('error.html', error='Unauthorized Access')

@routes.route('/showSignin')
def showSignin():
    """
    Loading sign in page
    :return: sign in template
    """
    return render_template('signin.html')

@routes.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
@routes.route('/forgotPassword')
def forgotPassword():
    return render_template('forgot_password.html')

@routes.route('/updateDevice', methods=['POST'])
def updateDevice():
    """
    Handling update device info request
    :return: response message
    """
    res = "Update device failed"
    try:
        device = filterSpecificObject(Device, macAddress=request.form['inputMacAddress'])
        device.name = request.form['inputDeviceName']
        device.owner = request.form['inputOwner']
        device.phoneNumber = request.form['inputPhoneNumber']
        device.osVersion = request.form['inputOsVersion']
        device.account =  request.form['inputAccount']
        device.macAddress = request.form['inputMacAddress']
        commitChanges()
        res = {'message':'Device updated successfully'}
    except Exception as e:
        logger.warning(e)
        res = {'error': 'Failed to update device'}
    finally:
        return jsonify(res)

@routes.route('/createDevice', methods=['POST'])
def createDevice():
    """
    Creating new device record, on success,
    render home page
    :return:
    """
    try:
        res = {}
        if (filterSpecificObject(Device, macAddress=request.form['inputMacAddress'])):
            res = {'error':'Device already exists'}
        else:

            device = Device(request.form['inputDeviceName'],
                            request.form['inputAccount'],
                            request.form['inputMacAddress'],
                            request.form['inputPhoneNumber'],
                            request.form['inputOwner'],
                            request.form['inputOs'],
                            request.form['inputOsVersion'])
            addObject(device)
            res = {'message':'Device created successfully'}
    except Exception as e:
        logger.warning(e)
        res = {'error':'Failed to create device'}
    finally:
        return jsonify(res)

@routes.route('/signUp', methods=['POST'])
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

@routes.route('/validateLogin', methods=['POST'])
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

@routes.route('/lockDevice', methods=['POST'])
def lockDevice():
    try:
        res = {'error': 'Failed to lock device'}
        device = filterSpecificObject(Device,
                                      macAddress=request.values.get('mac_address',None))
        if device:
            device.owner = session.get('userName')
            commitChanges()
            user = filterSpecificObject(User,
                                        username=session.get('userName'))
            addObject(History(datetime.now(),
                              user.username, "Locked " + device.name + "(" + device.macAddress + ")"))
            res = {'message':'Device locked'}
    except Exception as e:
        logger.warning(e)
        return jsonify(res)
    finally:
        return jsonify(res)

@routes.route('/unlockDevice', methods=['POST'])
def unlockDevice():
    try:
        res = {'error': 'Failed to unlock device'}
        device = filterSpecificObject(Device,
                                      macAddress=request.values.get('mac_address', None))
        if device:
            device.owner = ''
            commitChanges()
            user = filterSpecificObject(User,
                                        username=session.get('userName'))
            addObject(History(datetime.now(),
                              user.username, "Unlocked " + device.name + "(" + device.macAddress + ")"))
            res = {'message':'Device unlocked', 'title':'Unlocked'}
    except Exception as e:
        logger.warning(e)
    finally:
        return jsonify(res)

@routes.route('/resetPassword', methods=['POST'])
def resetPassword():
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

@routes.route('/resetPassword/<token>')
def authToken(token):
    user = User.verify_auth_token(token)
    if not user:
        return render_template('error.html', error='Unauthorized Access')
    return render_template('reset_password.html', token=token)

@routes.route('/updatePassword',methods=['POST'])
def updatePassword():
    user = User.verify_auth_token(request.values.get('token', None))
    if not user:
        return jsonify({'error':'Failed to update password'})
    hashed_password = generate_password_hash(request.values.get('password', None))
    user.password = hashed_password
    commitChanges()
    return jsonify({'message':'Password updated','title':'Update'})

@routes.route('/getUserNamesList', methods=['GET', 'POST'])
def getUsersNameList():
    res = selectObject(User, User.username, isDeleted=0)
    users = {'users':[]}
    for user in res:
        users['users'].append(user['username'])
    print users
    return jsonify(users)

@routes.route('/updateUser', methods=['POST'])
def updateUser():
    user = filterSpecificObject(User,
                                username=request.values.get('username', None))
    if user:
        user.role = request.values.get('role', 'guest')
        commitChanges()
        return jsonify({'message':'User role updated'})
    return jsonify({'error':'Failed to update user role'})

@routes.route('/deleteUser', methods=['POST'])
def deleteUser():
    user = filterSpecificObject(User,
                                username=request.values.get('username', None))
    if user:
        setObjectIsDeleted(user)
        return jsonify({'message':'User deleted',
                        'title':'Deleted'})
    return jsonify({'error':'Failed to delete user'})

@routes.route('/showHistory')
def showHistory():
    if session.get('user'):
        return render_template('history.html',
                               role=session.get('role'),
                               user=session.get('user'),
                               username=session.get('userName')
                               )
    else:
        return render_template('error.html', error='Unauthorized Access')

@routes.route('/getHistoryEvents', methods=['POST'])
def getUserActionsHistory():
    startEventDate = datetime.strptime(request.values.get('date', None), '%Y-%m-%d')
    endEventDate = startEventDate.replace(minute=59, hour=23, second=59)
    if startEventDate:
        results = getEventsHistory(History, startEventDate, endEventDate)
        event = {}
        events = []
        for e in results:
            event["startTime"] = datetime.strftime(e.executed_on, '%H:%M')
            event["text"] = str(e.user_id).split("@")[0]+" "+e.action
            events.append(event.copy())
        return jsonify({'events':events})
    return jsonify({'error':'Failed to get events'})

