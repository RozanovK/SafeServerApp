import datetime
import hashlib
import socket

import pymysql


########## get_ip() only for test on localhost (get own IP), to get IP of client use env variables

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP



def checkAuth(login, passwd):
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)
    #ip = os.environ["REMOTE_ADDR"] only for CGI
    ip = getIP()
    db = pymysql.connect("localhost", "rozanovk", "siema", "login")
    cursor = db.cursor()
    pwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    cursor.execute('SELECT password FROM users WHERE login = "%s" AND password = "%s"' % (login, pwd))
    results = str(cursor.fetchone()[0])
    if results == pwd:
        cursor.execute('''INSERT INTO logs (ip, login, time, validation) VALUES (%s, %s, %s, %s)''' , (ip, login, time, "Y"))
        db.commit()
        return True
    else:
        cursor.execute('''INSERT INTO logs (ip, login, time, validation) VALUES (%s, %s, %s, %s)''' , (ip, login, time, "N"))
        db.commit()
        return False

    db.close()












