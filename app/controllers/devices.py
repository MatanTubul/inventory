
from datetime import datetime
from flask import render_template, \
    Blueprint, \
    request, \
    session, \
    jsonify

from app import app
from app.models import User, Device, History
from app.database.utils import getDevicesList, \
    filterSpecificObject, \
    setObjectIsDeleted, \
    commitChanges, \
    addObject

import logging



logger = logging.getLogger(app.config['LOG_FILE'])
devices = Blueprint('devices',
                   __name__,
                   template_folder='templates')

@devices.route("/")
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

@devices.route('/userHome', methods=['GET','POST'])
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
        return render_template('signin.html')

@devices.route('/createDevice', methods=['POST'])
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
                            request.form['inputGroup'],
                            request.form['inputOwner'],
                            request.form['inputOs'],
                            request.form['inputOsVersion'])
            addObject(device)
            if(request.form['inputOwner']):
                addObject(History(datetime.now(),
                                  request.form['inputOwner'], "Locked " + device.name + "(" + device.macAddress + ")"))
            res = {'message':'Device created successfully'}
    except Exception as e:
        logger.warning(e)
        res = {'error':'Failed to create device'}
    finally:
        return jsonify(res)

@devices.route('/updateDevice', methods=['POST'])
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
        device.group = request.form['inputGroup']
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

@devices.route('/lockDevice', methods=['POST'])
def lockDevice():
    """
    Handling lock device request, in case is not locked device attached to user
    :return: json response
    """
    try:
        res = {'error': 'Failed to lock device'}
        device = filterSpecificObject(Device,
                                      macAddress=request.values.get('mac_address',None))
        if device:
            if not device.owner:
                device.owner = session.get('userName')
                commitChanges()
                user = filterSpecificObject(User,
                                            username=session.get('userName'))
                addObject(History(datetime.now(),
                                  user.username, "Locked " + device.name + "(" + device.macAddress + ")"))
                res = {'message':'Device locked'}
            else:
                res = {'error':'Device already locked!!!'}
    except Exception as e:
        logger.warning(e)
        return jsonify(res)
    finally:
        return jsonify(res)

@devices.route('/unlockDevice', methods=['POST'])
def unlockDevice():
    """
    Unlock device, detach device from a specific user.
    :return: json response
    """
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

@devices.route('/deleteDevice', methods=['POST'])
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