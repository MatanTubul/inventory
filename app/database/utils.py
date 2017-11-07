from app import db
from sqlalchemy import and_


def dbSetup():
    db.create_all()

def getDevicesList(object):
    return [u.__dict__ for u in db.session.query(object).filter_by(isDeleted=0).all()]

def getUsersList(object):
    return [u.__dict__ for u in db.session.query(object).filter_by(isDeleted=0).all()]

def filterSpecificObject(object, **kwargs):
    query = db.session.query(object)
    for key, value in kwargs.iteritems():
        query = query.filter(getattr(object, key) == value)
    return query.first()

def getEventsHistory(history, startTime, endTime):
    return db.session.query(history).filter(
        and_(history.executed_on >= startTime,
             history.executed_on <= endTime)).all()


def setObjectIsDeleted(object):
    object.isDeleted = 1
    commitChanges()

def commitChanges():
    db.session.commit()

def addObject(object):
    db.session.add(object)
    commitChanges()

def selectObject(object, *kwargs):
    return db.session.query(object).with_entities(*kwargs).all()

def updateObject(object, updateDict):
    db.session.query(object).update(updateDict)
    commitChanges()