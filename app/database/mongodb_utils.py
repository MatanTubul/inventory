
from reports.android import android_report
from reports.blue_apple import blue_apple_report
from reports.gold_apple import gold_apple_report
from reports.orange_apple import orange_apple_report
from reports.stripper_report_schema import stripper
from reports.avi import avi_report
from datetime import datetime
from collections import OrderedDict
from bson.codec_options import CodecOptions

#TODO add basic abilities to report
reports_dict = {"gold_apple":gold_apple_report,
                "blue_apple":blue_apple_report,
                "gallery":android_report,
                "stripper":stripper,
                "avi":avi_report,
                "orange_apple":orange_apple_report}

def buildReport(attack, osVersion, data=None, attackProccess=None, issues={}):

    report = reports_dict[attack]
    if not data:
        data = report["data"]
        if 'attackProccess' in report:
            attackProccess = report["attackProccess"]

    d = OrderedDict()
    d["_id"] = osVersion
    d["updated_on"] = str(datetime.strftime(datetime.now(), '%Y-%m-%d'))
    if attackProccess:
        d["attackProccess"] = attackProccess
    d["data"] = data
    d["issues"] = {}
    if attackProccess:
        for k, v in attackProccess.items():
            d["attackProccess"][k] = v
    for k, v in data.items():
        d["data"][k] = v

    for k, v in issues.items():
        d["issues"][k] = v
    print d["issues"]
    return d

def createCollection(mongo,name):
    options = CodecOptions(document_class=OrderedDict)
    return mongo.db[name].with_options(codec_options=options)

