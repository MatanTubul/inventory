from flask import render_template, \
    Blueprint, \
    request, \
    redirect,\
    session, \
    json
from werkzeug import generate_password_hash, check_password_hash

from app import app
from app.db import DbConnection

db = DbConnection(app)
cursor = db.getCursor()
routes = Blueprint('controllers',
                   __name__,
                   template_folder='templates')

@routes.route("/")
def main():
    # if session is active redirect to home page
    if session.get('user'):
        cursor.callproc('get_devices_list')
        devicesList = cursor.fetchall()
        return render_template('userHome.html', devices = devicesList,
                               role=session.get('role'),
                               user=session.get('userName')
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
        cursor.callproc('get_devices_list')
        devicesList = cursor.fetchall()
        return render_template('userHome.html',
                               devices = devicesList,
                               role=session.get('role'),
                               user=session.get('userName')
                               )
    else:
        return render_template('error.html', error = 'Unauthorized Access')

@routes.route('/deleteDevice', methods=['POST'])
def deleteDevice():
    """
    Handling delete device record request, in case of succesful,
    home page got render, otherwise popup message appear
    :return: response message
    """
    try:
        mac = request.values.get('mac_address', None)
        cursor.callproc('delete_device',(mac,))
        db.getConnection().commit()
        if cursor.rowcount > 0:
            return "Device deleted successfully"
        return "Delete device failed"
    except Exception as e:
        print e

@routes.route('/showSignUp')
def showSignUp():
    return render_template('signup.html', user=session.get('userName'))

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

        name = request.form['inputDeviceName']
        account = request.form['inputAccount']
        owner = request.form['inputOwner']
        phoneNumber = request.form['inputPhoneNumber']
        osVersion = request.form['inputOsVersion']
        macAddress = request.form['inputMacAddress']

        cursor.callproc('update_device', (name,
                                          account,
                                          owner,
                                          osVersion,
                                          macAddress,
                                          phoneNumber))
        db.getConnection().commit()
        if cursor.rowcount > 0:
            res = "Device updated successfully"
    except Exception as e:
        print e
    finally:
        return res

@routes.route('/createDevice', methods=['POST'])
def createDevice():
    """
    Creating new device record, on success,
    render home page
    :return:
    """
    name = request.form['inputDeviceName']
    account = request.form['inputAccount']
    macAddress = request.form['inputMacAddress']
    phoneNumber = request.form['inputPhoneNumber']
    owner = request.form['inputOwner']
    os = request.form['inputOs']
    osVersion = request.form['inputOsVersion']

    cursor.callproc('createDevice', (name, account, macAddress,
                                     phoneNumber,owner, os,
                                     osVersion))
    data = cursor.fetchall()
    if len(data) is 0:
        db.getConnection().commit()
        cursor.callproc('get_devices_list')
        devicesList = cursor.fetchall()
        # return render_template('userHome.html', devices = devicesList)
        return "ok"
    else:
        return json.dumps({'error': str(data[0])})

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
        cursor.callproc('createUser', (email,
                                       hashed_password,
                                       name,
                                       role))
        db.getConnection().commit()
        data = cursor.fetchall()
        if len(data) == 0:
            res = {'message': 'User created successfully !'}

    except Exception as e:
        print e
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
        cursor.callproc('loginValidate',(username,))
        data = cursor.fetchall()
        if len(data) > 0:
            if check_password_hash(str(data[0][2]), password):
                session['user'] = data[0][0]
                session['userName'] = data[0][3]
                session['role'] = data[0][4]
                return json.dumps({'url':'http://localhost:5000/userHome'})
            else:
                return json.dumps({'error':'Wrong Email address or Password.'})
        else:
            return json.dumps({'error':'Wrong Email address or Password.'})
    except Exception as e:
        print e