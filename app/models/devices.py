from app import db

class Device(db.Model):
    __tablename__ = 'devices'
    name = db.Column(db.String(30))
    account = db.Column(db.String(256))
    macAddress = db.Column(db.String(64), index=True, primary_key=True)
    phoneNumber = db.Column(db.String(20))
    owner = db.Column(db.String(30))
    os = db.Column(db.String(30))
    osVersion = db.Column(db.String(30))
    isDeleted = db.Column(db.Boolean)

    def __init__(self, name,
                 account,
                 macAdress,
                 phone,
                 owner,
                 os,
                 osVersion,
                 isDeleted=False):
        self.name = name
        self.account = account
        self.macAddress = macAdress
        self.phoneNumber = phone
        self.owner = owner
        self.os = os
        self.osVersion = osVersion
        self.isDeleted = isDeleted

    def __repr__(self):
        return '<Device %r>' % (self.name)