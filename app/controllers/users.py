from flask import Blueprint, \
    request, \
    jsonify

from app import app
from app.models import User
from app.database.utils import filterSpecificObject, \
    setObjectIsDeleted, \
    commitChanges, \
    selectObject
import logging

logger = logging.getLogger(app.config['LOG_FILE'])
users = Blueprint('users',
                   __name__,
                   template_folder='templates')

@users.route('/getUserNamesList', methods=['GET', 'POST'])
def getUsersNameList():
    """
    Retrives users list
    :return:
    """
    res = selectObject(User, User.username, isDeleted=0)
    users = {'users':[]}
    for user in res:
        users['users'].append(user['username'])
    return jsonify(users)

@users.route('/updateUser', methods=['POST'])
def updateUser():
    """
    Updating user role
    :return:
    """
    user = filterSpecificObject(User,
                                username=request.values.get('username', None))
    if user:
        user.role = request.values.get('role', 'guest')
        commitChanges()
        return jsonify({'message':'User role updated'})
    return jsonify({'error':'Failed to update user role'})

@users.route('/deleteUser', methods=['POST'])
def deleteUser():
    """
    Revoke user from the system
    :return:
    """
    user = filterSpecificObject(User,
                                username=request.values.get('username', None))
    if user:
        setObjectIsDeleted(user)
        return jsonify({'message':'User deleted',
                        'title':'Deleted'})
    return jsonify({'error':'Failed to delete user'})