import hashlib
import os
import uuid

import passwordmeter

from pysql import database_connect, questions
from snippet import get_all_snipets
from vial import render_template


def signup_db(headers, body, data):
    db, cursor = database_connect()
    login = str(data['name']) if 'name' in data else ''
    password = str(data['pw']) if 'pw' in data else ''
    password_conf = str(data['pwconf']) if 'pwconf' in data else ''
    answer = str(data['answer']) if 'answer' in data else ''

    cursor.execute('SELECT * FROM users WHERE login=%s', (login))
    questions_tuple = questions()
    if (cursor.fetchone()) is not None:
        return render_template('signup.html', body=body, data=data, questions=questions_tuple,
                               message='This login is already in use, please choose another one!'), 200, {}
    if not check_login_char(login):
        return render_template('signup.html', body=body, data=data, questions=questions_tuple,
                               message='Login can only contains lowarcase letters!'), 200, {}
    if not check_login_length(login):
        return render_template('signup.html', body=body, data=data, questions=questions_tuple,
                               message='Login is too long!'), 200, {}
    if not (password == password_conf):
        return render_template('signup.html', body=body, data=data, questions=questions_tuple,
                               message='Passwords are not match!'), 200, {}
    strength, improvements = passwordmeter.test(password)

    if strength < 0.3:
        return render_template('signup.html', body=body, data=data, questions=questions_tuple,
                               message='Your password is too weak!'), 200, {}
    create_user_folder(login)
    salt = uuid.uuid4().hex
    salt_bytes = salt.encode('utf-8')

    for i in range(3):
        answer_bytes = answer.encode('utf-8')
        pw_bytes = password.encode('utf-8')
        password = hashlib.sha512(pw_bytes + salt_bytes).hexdigest()
        answer = hashlib.sha512(answer_bytes + salt_bytes).hexdigest()
    cursor.execute('INSERT INTO users(login, password, salt, answer) VALUES (%s, %s, %s, %s)',
                   (login, password, salt, answer))
    db.commit()
    db.close()
    snippets = get_all_snipets()
    return render_template('index.html', body=body, data=data, snippets=snippets,
                           message='You successfully registered new user!'), 200, {}


def check_login_char(login):
    for i in login:
        if not i.islower():
            return False
    return True


def check_login_length(login):
    if len(login) > 20:
        return False
    return True


def create_user_folder(login):
    currDir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(currDir + "/../serwer/usr/" + login)
