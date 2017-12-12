from app import db

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    executed_on = db.Column(db.DateTime())
    user_id = db.Column(db.String(30), db.ForeignKey('users.username'), nullable=False)
    action = db.Column(db.String(120), nullable=False)



    def __init__(self, time, user_id, action):
        self.executed_on = time
        self.user_id = user_id
        self.action = action

    def __repr__(self):
        return '<Action %r>' % (self.action)