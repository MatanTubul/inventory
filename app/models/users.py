
from app import db, app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(30), index=True, primary_key=True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(64))
    role = db.Column(db.String(20))

    def __init__(self, username, password, name, role):
        self.username = username
        self.password = password
        self.name = name
        self.role = role

    def __repr__(self):
        return '<User %r>' % (self.username)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.username})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user