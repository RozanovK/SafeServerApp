from __future__ import print_function

import hashlib
import random
import socket

import pysql
from snippet import get_snippet
from vial import render_template


def get_own_ip():
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
    if check_auth(login, passwd):
        if ban_ip(login):
            IP, time = print_ip(login)
            d_t, title, snippet = get_snippet(login)
            token = create_token()
            cookie = '{0}; expires: Thu, 18 Dec 2017 12:00:00 UTC; secure'.format(token)
            return render_template('mainpage.html', headers = headers, body=body, data=data, IP= IP, time=time,d_t =d_t, title=title, snippets = snippet), 200,  {'Set-Cookie': cookie}
        else:
            return render_template('ban.html', body=body, data=data)
    else:
        return render_template('index.html', headers=headers, body=body, data=data,
                               message='Login or password is incorrect'), 200, {}


def check_auth(login, passwd):
    #ip = get_client_address()
    ip = get_own_ip()
    pwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()

    db, cursor = pysql.database_connect()
    cursor.execute('SELECT password FROM users WHERE login = %s' , login)
    results = str(cursor.fetchone()[0])
    if results == pwd:
        insert_log(ip, login, "Y")
        return True
    else:
         insert_log(ip, login, "N")
         return False


def ban_ip(login):
    db,cursor = pysql.database_connect()
    cursor.execute(
        '''SELECT COUNT(*) FROM logs WHERE validation="N" AND login = %s AND (TIMESTAMPDIFF(HOUR, time, Now()) < 1)''',
        login)  # sprawdzamy ilość niepoprawnych walidacji w ciągu ostatniej godziny
    num = int(str(cursor.fetchone()[0]))
    if num < 5:
        return True
    else:
        return False


def insert_log(ip, login, validation):
    time = pysql.datetime_mysql()

    db, cursor = pysql.database_connect()
    cursor.execute('''INSERT INTO logs (ip, login, time, validation) VALUES (%s, %s, %s, %s)''', (ip, login, time, validation))
    db.commit()
    db.close


def print_ip(login):
    db, cursor = pysql.database_connect()
    cursor.execute('''SELECT ip, time from logs WHERE login = %s AND validation = "N"''', login)
    #logowania = cursor.fetchall()
    #for i in logowania:
    #    IP, datetime = logowania[0]
    logowania = cursor.fetchall()
    IP, datetime = logowania[0]
    return IP, datetime


def get_login(data):
    login = str(data['name']) if 'name' in data else ''


def forgot_password(headers, body, data):      #check if login exists in database
    login = str(data['name']) if 'name' in data else ''
    answer_entered = str(data['answer']) if 'answer' in data else ''
    login_newpass = login

    db, cursor = pysql.database_connect()
    cursor.execute('''SELECT * from users WHERE login = %s ''', login)

    if str(cursor.fetchone()[0]) != 0:
        cursor.execute('''SELECT answer FROM users WHERE login = %s''', login)
        answerdb = str(cursor.fetchone()[0])
        a = hashlib.sha256(answer_entered.encode('utf-8')).hexdigest()
        if answerdb == a:
            return render_template('passwordchange.html', body=body, data=data, login=login), 200, {}
        else:
            return render_template('wronganswer.html', body=body, data=data), 200, {}
    else:
        return render_template('wronganswer.html', body=body, data=data), 200, {}


def insert_new_password(headers, body, data):
    login = str(data['name']) if 'name' in data else ''
    passwd = str(data['pw']) if 'pw' in data else ''
    passwd_r = str(data['pw-x']) if 'pw-x' in data else ''
    pw = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    if passwd == passwd_r:
        db, cursor = pysql.database_connect()
        cursor.execute('''UPDATE users SET password= %s WHERE login= %s''', (pw, login))
        db.commit()
        db.close()
        return render_template('successfull_pw_change.html', body=body, data=data), 200, {}
    else:
        return False


def questions():
    db, cursor = pysql.database_connect()
    cursor.execute('''SELECT * FROM questions''')
    questions = cursor.fetchall()
    db.close()
    return questions


def create_token():
    import string
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(random.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3):
            break
    return password
