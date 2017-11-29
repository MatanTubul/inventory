
from reports.android import android_report
from reports.blue_apple import blue_apple_report
from reports.gold_apple import gold_apple_report
from reports.orange_apple import orange_apple_report
from reports.avi import avi_report
from datetime import datetime
from collections import OrderedDict
from bson.codec_options import CodecOptions
import bson


#TODO add basic abilities to report
reports_dict = {"gold_apple":gold_apple_report,
                "blue_apple":blue_apple_report,
                "gallery":android_report,
                "stripper":orange_apple_report,
                "avi":avi_report}

def buildReport(attack, osVersion):
    report = reports_dict[attack]
    d = OrderedDict()
    d["_id"] = ""
    d["updated_on"] = ""
    d["attackProccess"] = {}
    d["data"] = {}
    for k, v in report["attackProccess"].items():
        d["attackProccess"][k] = v
    for k, v in report["data"].items():
        d["data"][k] = v
    d["issues"] = {}
    d["_id"] = osVersion
    d["updated_on"] = str(datetime.strftime(datetime.now(), '%Y-%m-%d'))
    return d

def createCollection(mongo,name):
    options = CodecOptions(document_class=OrderedDict)
    return mongo.db[name].with_options(codec_options=options)

