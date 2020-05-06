from flask import render_template, Blueprint, jsonify
from app import app
from app.models import Account
import logging
from app.database.utils import getAccountsList, addObject, commitChanges,filterSpecificObject
from app.utils import Utils

logger = logging.getLogger(app.config['LOG_FILE'])
account = Blueprint('accounts',
                   __name__,
                   template_folder='templates')

apps = {
  "Facebook": {
    "username": "",
    "password": ""
  },
  "Gmail": {
    "username": "",
    "password": ""
  },
  "Outlook": {
    "username": "",
    "password": ""
  },
  "MailRu": {
    "username": "",
    "password": ""
  },
  "GMX": {
    "username": "",
    "password": ""
  },
  "Skype": {
    "username": "",
    "password": ""
  },
  "DropBox": {
    "username": "",
    "password": ""
  },
  "Instagram": {
    "username": "",
    "password": ""
  },
  "Twitter": {
    "username": "",
    "password": ""
  },
  "Yahoo": {
    "username": "",
    "password": ""
  },
  "SnapChat": {
    "username": "",
    "password": ""
  },
  "Icloud": {
    "username": "",
    "password": ""
  }
}
@account.route('/loadAccounts/<mac>/<account>/<dname>')
def loadAccounts(mac, account, dname):
    """load all accounts which assigned to specific device

    """
    try :
        accounts = getAccountsList(Account, mac)
        if len(accounts) < 1:
            createBaseAccount(mac, account)
            accounts = getAccountsList(Account, mac)

        return render_template('accounts.html', accounts=accounts, mac=mac, device_name= dname, account=account)
    except Exception as e:
        logger.warning(e)

@account.route('/updateAccounts',methods=['POST'])
def updateAccounts():
    """
    update existing accounts
    :return:
    """
    try :
        json_data = Utils.getRequestJSON()
        for account in json_data["accounts"]:
            stored_account = filterSpecificObject(Account, macAddress=json_data["mac"],app=account)
            stored_account.username = json_data["accounts"][account]["username"]
            stored_account.password = json_data["accounts"][account]["password"]
            commitChanges()
        return jsonify({'message' :'Accounts updated'})
    except Exception as e:
        logger.warning(e)
        return {'error': "Failed to update accounts"}

@account.route('/createAccount',methods=['POST'])
def createAccount():
    """
    Add new app to Accounts list
    :return:
    """
    try :
        json_data = Utils.getRequestJSON()
        account = Account(json_data["mac"],
                          json_data["app"],
                          json_data["username"],
                          json_data["password"])
        addObject(account)
        return jsonify({'message' :'Account created'})
    except Exception as e:
        logger.warning(e)
        return {'error' :"Failed to create account"}


def createBaseAccount(mac , account):
    for app, value in apps.iteritems():
        addObject(Account(mac,
                          app,
                          account,
                          value["password"]))


