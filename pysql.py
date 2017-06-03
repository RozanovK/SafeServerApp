import pymysql
from datetime import datetime

DATABASE_HOST = 'localhost'
DATABASE_LOGIN = 'rozanovk'
DATABASE_PASSWORD = 'siema'
DATABASE_NAME = 'login'


def database_connect():
    db = pymysql.connect(DATABASE_HOST, DATABASE_LOGIN, DATABASE_PASSWORD, DATABASE_NAME)
    cursor = db.cursor()
    return db, cursor


#convert Python datetype to MySql datetime
def datetime_mysql():
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.now().strftime(f)
    return time