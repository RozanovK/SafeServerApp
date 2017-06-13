import hashlib
import uuid

import passwordmeter

import pysql
from pysql import questions
from snippet import get_all_snipets
from vial import render_template


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
        salt_bytes = salt.encode('utf-8')
        db.close()
        for i in range(3):
            a_bytes = a.encode('utf-8')
            a = hashlib.sha512(a_bytes + salt_bytes).hexdigest()
        if answerdb == a:
            return render_template('passwordchange.html', body=body, data=data, login=login), 200, {}
        else:
            questions_tuple = questions()
            return render_template('recovery.html', body=body, data=data, message='Wrong answer!',
                                   questions=questions_tuple), 200, {}
    else:
        db.close()
        questions_tuple = questions()
        return render_template('recovery.html', body=body, data=data, message='Wrong answer!',
                               questions=questions_tuple), 200, {}


def insert_new_password(headers, body, data):
    login = str(data['name']) if 'name' in data else ''
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
        db, cursor = pysql.database_connect()
        cursor.execute('''UPDATE users SET password= %s, salt= %s WHERE login= %s''', (passwd, salt, login))
        db.commit()
        db.close()
        snippets = get_all_snipets()
        return render_template('index.html', body=body, data=data, snippets=snippets,
                               message='You successfully changed your password!'), 200, {}
    else:
        return render_template('passwordchange.html', body=body, data=data, login=login,
                               message='Passwords are not match!'), 200, {}
