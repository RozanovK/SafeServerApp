from __future__ import print_function

import hashlib

import pysql
from cookie import AuthCookieFactory
from snippet import get_all_snipets
from vial import render_template


def auth(headers, body, data):
    login = str(data['name']) if 'name' in data else ''
    passwd = str(data['pw']) if 'name' in data else ''
    # ip = str(headers['http-x-forwarded-for']) if 'http-x-forwarded-for' in headers else 'PROXY'
    ip = str(headers['remote-addr'])
    if check_auth(login, passwd, ip):
        if ban_ip(login):
            IP, time = pysql.print_ip(login)
            db, cursor = pysql.database_connect()
            cookie = (AuthCookieFactory()).generate()
            cursor.execute('INSERT INTO cookie(login, token) VALUES(%s, %s)', (login, cookie.get_token()))
            db.commit()
            db.close()
            return render_template('mainpage.html', headers=headers, body=body, data=data, IP=IP, time=time), 200, {
                'Set-Cookie': cookie.return_cookie()}
        else:
            snippets = get_all_snipets()
            return render_template('index.html', body=body, data=data, snippets=snippets,
                                   message='Too many wrong attemts to log in! You\'ve banned!')
    else:
        snippets = get_all_snipets()
        return render_template('index.html', headers=headers, body=body, data=data, snippets=snippets,
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








