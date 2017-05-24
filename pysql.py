import datetime
import hashlib
import socket
import sys
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
    db = pymysql.connect("localhost", "rozanovk", "siema", "login")
    cursor = db.cursor()
    cursor.execute(
        '''SELECT COUNT(*) FROM logs WHERE validation="N" AND login = %s AND (TIMESTAMPDIFF(HOUR, time, Now()) < 1)''', login) #sprawdzamy ilość niepoprawnych walidacji w ciągu ostatniej godziny
    num = int(str(cursor.fetchone()[0]))
    if num > 5:
        print("Too many log in attempts from your's IP. You've banned for an hour")
        sys.exit()
    # ip = os.environ["REMOTE_ADDR"] only for CGI
    ip = getIP()
    pwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    cursor.execute('SELECT password FROM users WHERE login = "%s"' % login)
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


def printIP(login):
    db = pymysql.connect("localhost", "rozanovk", "siema", "login")
    cursor = db.cursor()
    cursor.execute('''SELECT ip, time from logs WHERE login = %s AND validation = "N"''', login)
    logowania = cursor.fetchall()
    for i in logowania:
        IP, datetime = logowania[0]
        print('There was unsuccessful login attempt from IP %s at %s' % (IP, datetime))














