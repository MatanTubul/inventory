#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
#
# engine = create_engine('mysql://root:edco123@localhost', convert_unicode=True)
#
# # Query for existing databases
# existing_databases = engine.execute("SHOW DATABASES;")
# # Results are a list of single item tuples, so unpack each tuple
# existing_databases = [d[0] for d in existing_databases]
# # Create database if not exists
#
#
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()
#
# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     import app.models
#     if 'wintventory' not in existing_databases:
#         engine.execute("CREATE DATABASE IF NOT EXISTS wintventory")  # create db
#     engine.execute("USE wintventory")  # select new db
#     connection = engine.raw_connection()
#     cursor = connection.cursor()
#     cursor.execute("show tables")
#     for r in cursor.fetchall():
#         print r[0]
#     Base.metadata.create_all(bind=engine)
#     return cursor
#
# # class DbConnection():
# #
# #     def __init__(self,app):
# #         # mysql = MySQL()
# #         # app.config['MYSQL_DATABASE_USER'] = 'root'
# #         # app.config['MYSQL_DATABASE_PASSWORD'] = 'edco123'
# #         # app.config['MYSQL_DATABASE_DB'] = 'inventory'
# #         # app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# #         app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:edco123@localhost/inventory'
# #         # mysql.init_app(app)
# #         self.conn = SQLAlchemy(app)
# #         # self.cursor = self.conn.cursor()
# #
# #     def getConnection(self):
# #         return self.conn
# #
# #     # def getCursor(self):
# #     #     return self.cursor