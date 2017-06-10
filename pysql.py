from datetime import datetime

import pymysql

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


def questions():
    db, cursor = database_connect()
    cursor.execute('''SELECT * FROM questions''')
    questions = cursor.fetchall()
    db.close()
    return questions


def print_ip(login):
    db, cursor = database_connect()
    cursor.execute('''SELECT ip, time from logs WHERE login = %s AND validation = "N"''', login)
    # logowania = cursor.fetchall()
    # for i in logowania:
    #    IP, datetime = logowania[0]
    logowania = cursor.fetchall()
    if logowania is None:
        return None, None
    IP, datetime = logowania[0]
    return IP, datetime
