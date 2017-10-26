import argparse

from flask import Flask, render_template, request, redirect
from flask import session
from flask import json
from db import DbConnection
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

db = DbConnection(app)
cursor = db.getCursor()
app.secret_key = 'r?4#/FUKr6u;Vh<s|d1:6-NPg^Rhy]'


@app.route("/")
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

@app.route('/userHome', methods=['GET','POST'])
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

@app.route('/deleteDevice', methods=['POST'])
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

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html', user=session.get('userName'))

@app.route('/showSignin')
def showSignin():
    """
    Loading sign in page
    :return: sign in template
    """
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
@app.route('/forgotPassword')
def forgotPassword():
    return render_template('forgot_password.html')

@app.route('/updateDevice', methods=['POST'])
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

@app.route('/createDevice', methods=['POST'])
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

@app.route('/signUp', methods=['POST'])
def signUp():
    """
    # read signUp values from UI
    :return:
    """
    try:
        name = request.form['inputName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        hashed_password = generate_password_hash(password)
        # validate the received values
        cursor.callproc('createUser', (email, hashed_password, name))
        data = cursor.fetchall()
        if 'Username Exists !!' != data[0][0]:
            db.getConnection().commit()
            return json.dumps({'message': 'User created successfully !'})
        else:
            return json.dumps({'error': str(data[0][0])})
    except Exception as e:
        print e



@app.route('/validateLogin', methods=['POST'])
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


def argsPars():
    parser = argparse.ArgumentParser(description='Wintventory web server')
    parser.add_argument('--host', type=str, default="localhost", help='DB host url.', metavar='')
    parser.add_argument('-p', '--port', type=int, default=5000, help='DB user.', metavar='')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = argsPars()
    app.run(debug=True,
            host=args.host,
            port=args.port)
