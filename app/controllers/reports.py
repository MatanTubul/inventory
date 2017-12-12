
from flask import render_template, \
    Blueprint, \
    redirect, \
    jsonify
from app import app, mongo
from app.models import Device
from app.database.utils import filterSpecificObject
from app.database.mongodb_utils import buildReport, createCollection
import logging
from app.utils import Utils

logger = logging.getLogger(app.config['LOG_FILE'])
report = Blueprint('reports',
                   __name__,
                   template_folder='templates')


@report.route('/loadDeviceReports/<mac>/<attack>')
def loadDeviceReports(mac, attack):
    """
    Load device reprot based on is os type
    :param mac: device mac address
    :param attack: default attack (IOS: gold_apple, Android: gallery, PC: Avi)
    :return: template with extra data
    """
    try:
        device =  filterSpecificObject( Device, macAddress=mac)
        os = device.os
        if device:
            collection =  createCollection( mongo, attack)
            report = collection.find_one({"_id": mac})
            # Device does not exist in the report
            if not report:
                schema = {"_id": mac,
                              "name":device.name,
                              "account":device.account,
                              "reports": [ buildReport(attack,
                                                      device.osVersion,
                                                      data=None,
                                                      attackProccess=None)]}
                collection.insert_one(schema)
            #in case device exist in reports but version not
            elif not collection.find_one({"_id": mac, "reports._id": device.osVersion}):
                collection.update_one({"_id" : mac},
                                      {'$push' : {"reports":  buildReport(attack,
                                                                          device.osVersion,
                                                                          data=None,
                                                                          attackProccess=None,
                                                                          issues={})}})

            report = collection.find_one({"_id": mac})

            return  render_template('reports.html', report=report,
                                   attack=attack,
                                   osType=os,
                                   deviceName = device.name)
    except Exception as e:
        logger.warning(e)
        return redirect("/", code=302)

@report.route('/updateReportDocument', methods=['POST','GET'])
def updateReportDocument():
    """
    Update sub document on report collection
    :return:
    """
    try :
        json_data =  Utils.getRequestJSON()
        attackProccess = None
        report_data = json_data['report']
        mac = json_data['mac']
        attack = json_data['attack']

        #get report osVersion
        osVersion = report_data["deviceName"].keys()[0]
        #get collection
        collection =  createCollection( mongo, attack)

        report = collection.find_one({"_id" : mac})
        data = report_data["deviceName"][osVersion]["data"]
        issues = report_data["deviceName"][osVersion]["issues"]
        if 'attackProccess' in report_data["deviceName"][osVersion]:
            attackProccess = report_data["deviceName"][osVersion]["attackProccess"]

        if report :
            report = collection.find_one({"_id": mac, "reports._id": osVersion})
            if report:
                print "update array object"
                collection.update_one({"_id": mac,"reports._id":osVersion},
                             {'$set':{"reports.0": buildReport(attack,
                                                              osVersion,
                                                              data=data,
                                                              attackProccess=attackProccess,
                                                              issues=issues)}})
            else:
                print "add new element to report array"
                collection.update_one({"_id": mac},
                                   {'$push':{"reports": buildReport(attack,
                                                                   osVersion,
                                                                   data=None,
                                                                   attackProccess=None,
                                                                   issues={})}})
            return  jsonify({'ok': "report updated"})

        return {'error': "Failed to update report"}
    except Exception as e :
        logger.warning(e)
        return  redirect("/", code=302)