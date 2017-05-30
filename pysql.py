from __future__ import print_function
from builtins import str
# -*- coding: utf-8 -*-
from vial import render_template, Vial
import cgi
import datetime
import hashlib
import socket
import sys
import pymysql
from os import environ
from vial import render_template


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


def auth(headers, body, data):

    login = str(data['name']) if 'name' in data else ''
    passwd = str(data['pw']) if 'name' in data else ''
    if checkAuth(login, passwd):
        return render_template('mainpage.html', body=body, data=data), 200, {}

def checkAuth(login, passwd):

    pwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    ip = getIP()
    # ip = os.environ["REMOTE_ADDR"] only for CGI

    db = pymysql.connect("localhost", "rozanovk", "siema", "login")
    cursor = db.cursor()
    cursor.execute('SELECT password FROM users WHERE login = "%s"' % login)
    results = str(cursor.fetchone()[0])
    if results == pwd:
        insertLog(ip, login, "Y")
        return True
    else:
         insertLog(ip, login, "N")
         return False

    db.close()




def banIP(login):

    db = pymysql.connect("localhost", "rozanovk", "siema", "login")
    cursor = db.cursor()
    cursor.execute(
        '''SELECT COUNT(*) FROM logs WHERE validation="N" AND login = %s AND (TIMESTAMPDIFF(HOUR, time, Now()) < 1)''',
        login)  # sprawdzamy ilość niepoprawnych walidacji w ciągu ostatniej godziny
    num = int(str(cursor.fetchone()[0]))
    if num > 5:
        print("Too many log in attempts from your's IP. You've banned for an hour")
        sys.exit()



def insertLog(ip, login, validation):

    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.datetime.now().strftime(f)

    db = pymysql.connect("localhost", "rozanovk", "siema", "login")
    cursor = db.cursor()
    cursor.execute('''INSERT INTO logs (ip, login, time, validation) VALUES (%s, %s, %s, %s)''', (ip, login, time, validation))
    db.commit()
    db.close


def loginAttempts():





