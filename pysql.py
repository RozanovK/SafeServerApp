import pymysql
import hashlib


def checkAuth(login, passwd):
    db = pymysql.connect("localhost", "rozanovk", "siema", "login")
    cursor = db.cursor()
    pwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    cursor.execute('SELECT password FROM users WHERE login = "%s" AND password = "%s"' % (login, pwd))
    results = str(cursor.fetchone()[0])
    db.close()
    if results == pwd:
        return True
    else:
        return False


