
from flaskext.mysql import MySQL
class DbConnection():

    def __init__(self,app):
        mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'edco123'
        app.config['MYSQL_DATABASE_DB'] = 'inventory'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)
        self.conn = mysql.connect()
        self.cursor = self.conn.cursor()

    def getConnection(self):
        return self.conn

    def getCursor(self):
        return self.cursor