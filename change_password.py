import hashlib
import uuid

import passwordmeter

import pysql
from cookie import AuthCookieFactory
from vial import render_template


def insert_new_passwd(headers, body, data):
    db, cursor = pysql.database_connect()

    token = str((AuthCookieFactory()).get_from_headers(headers).get_token())
    if token is None:
        return render_template('unauthorised_request.html', body=body, data=data,
                               message='Anauthorised try to change password!'), 200, {}
    cursor.execute('''SELECT login FROM cookie WHERE token=%s''', token)
    login = str(cursor.fetchone()[0])
    passwd = str(data['pw']) if 'pw' in data else ''
    passwd_r = str(data['pw-x']) if 'pw-x' in data else ''

    salt = uuid.uuid4().hex
    salt_bytes = salt.encode('utf-8')
    if passwd == passwd_r:
        strength, improvements = passwordmeter.test(passwd)
        if strength < 0.3:
            return render_template('passwordchange.html', body=body, data=data, login=login,
                                   message='Your password is too weak!'), 200, {}
        for i in range(3):
            pw_bytes = passwd.encode('utf-8')
            passwd = hashlib.sha512(pw_bytes + salt_bytes).hexdigest()
        cursor.execute('''UPDATE users SET password= %s, salt= %s WHERE login= %s''', (passwd, salt, login))
        db.commit()
        db.close()
        IP, time = pysql.print_ip(login)
        return render_template('mainpage.html', body=body, data=data, IP=IP, time=time,
                               message='You successfully changed your password!'), 200, {}
    else:
        return render_template('passwordchange.html', body=body, data=data,
                               message='Passwords are not match!'), 200, {}


def change_password_form(headers, body, data):
    return render_template('passwordchange_u.html', headers=headers, body=body, data=data), 200, {}
