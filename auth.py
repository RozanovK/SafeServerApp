from __future__ import print_function

import hashlib
import random
import uuid

import pysql
from snippet import get_snippet
from vial import render_template


def auth(headers, body, data):
    login = str(data['name']) if 'name' in data else ''
    passwd = str(data['pw']) if 'name' in data else ''
    # ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    ip = str(headers['remote-addr'])
    if check_auth(login, passwd, ip):
        if ban_ip(login):
            IP, time = print_ip(login)
            d_t, title, snippet = get_snippet(login)
            token = create_token()
            cookie = 'nazwa={0}; expires=Fri, 07-Jun-2019 19:40:00 GMT; Max-Age=63071999; path=/; domain=.od.com; secure;'.format(
                token)
            return render_template('mainpage.html', headers=headers, body=body, data=data, IP=IP, time=time, d_t=d_t,
                                   title=title, snippets=snippet), 200, {'Set-Cookie': cookie}
        else:
            return render_template('index.html', body=body, data=data,
                                   message='Too many wrong attemts to log in! You\'ve banned!')
    else:
        return render_template('index.html', headers=headers, body=body, data=data,
                               message='Login or password is incorrect'), 200, {}


def check_auth(login, password, ip):
    db, cursor = pysql.database_connect()

    cursor.execute('SELECT password FROM users WHERE login = %s', (login))
    x = cursor.fetchone()
    if (x) is None:
        return False
    results = str(x[0])
    cursor.execute('SELECT salt FROM users WHERE login = %s', (login))

    salt = str(cursor.fetchone()[0])
    salt_bytes = salt.encode('utf-8')
    for i in range(3):
        pw_bytes = password.encode('utf-8')
        password = hashlib.sha512(pw_bytes + salt_bytes).hexdigest()
    if results == password:
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


def forgot_password(headers, body, data):
    login = str(data['name']) if 'name' in data else ''
    a = str(data['answer']) if 'answer' in data else ''

    db, cursor = pysql.database_connect()
    cursor.execute('''SELECT * from users WHERE login = %s ''', login)

    if cursor.fetchone() is not None:
        cursor.execute('''SELECT answer FROM users WHERE login = %s''', login)
        answerdb = str(cursor.fetchone()[0])
        cursor.execute('SELECT salt FROM users WHERE login = %s', login)
        salt = str(cursor.fetchone()[0])
        db.close()
        if answerdb == a:
            pw_bytes = password.encode('utf-8')
            salt_bytes = salt.encode('utf-8')
            for i in range(3):
                hashed_password = hashlib.sha512(pw_bytes + salt_bytes).hexdigest()
            return render_template('passwordchange.html', body=body, data=data, login=login), 200, {}
        else:
            return render_template('passwordchange.html', body=body, data=data, message='Wrong answer!'), 200, {}
    else:
        db.close()
        return render_template('passwordchange.html', body=body, data=data, message='Wrong answer!'), 200, {}


def insert_new_password(headers, body, data):
    login = str(data['name']) if 'name' in data else ''
    passwd = str(data['pw']) if 'pw' in data else ''
    passwd_r = str(data['pw-x']) if 'pw-x' in data else ''

    salt = uuid.uuid4().hex
    pw_bytes = passwd.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    for i in range(3):
        hashed_password = hashlib.sha512(pw_bytes + salt_bytes).hexdigest()
    if passwd == passwd_r:
        db, cursor = pysql.database_connect()
        cursor.execute('''UPDATE users SET password= %s, salt= %s WHERE login= %s''', (hashed_password, salt, login))
        db.commit()
        db.close()
        return render_template('index.html', body=body, data=data,
                               message='You successfully changed your password!'), 200, {}
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
    sys_random = random.SystemRandom()
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(sys_random.choice(alphabet) for i in range(10))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3):
            break
    return password
