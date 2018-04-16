from app import db

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app = db.Column(db.String(256))
    username = db.Column(db.String(30))
    password = db.Column(db.String(256))

    macAddress = db.Column(db.String(64), db.ForeignKey('devices.macAddress'), nullable=False)

    def __init__(self, macAddress , app, username, password):
        self.macAddress = macAddress
        self.app = app
        self.username = username
        self.password = password


    def __repr__(self):
        return '<Account %r>' % (self.id)
