import hashlib
import uuid

import passwordmeter

from auth import questions
from pysql import database_connect
from vial import render_template


def signup_db(headers, body, data):
    db, cursor = database_connect()
    login = str(data['name']) if 'name' in data else ''
    password = str(data['pw']) if 'pw' in data else ''
    password_conf = str(data['pwconf']) if 'pwconf' in data else ''
    answer = str(data['answer']) if 'answer' in data else ''

    cursor.execute('SELECT * FROM users WHERE login=%s', (login))
    if (cursor.fetchone()) is not None:
        questions_tuple = questions()
        return render_template('signup.html', body=body, data=data, questions=questions_tuple,
                               message='This login is already in use, please choose another one!'), 200, {}
    if not (password == password_conf):
        questions_tuple = questions()
        return render_template('signup.html', body=body, data=data, questions=questions_tuple,
                               message='Passwords are not match!'), 200, {}
    strength, improvements = passwordmeter.test(password)

    if strength < 0.3:
        questions_tuple = questions()
        return render_template('signup.html', body=body, data=data, questions=questions_tuple,
                               message='Your password is too weak!'), 200, {}
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
    return render_template('index.html', body=body, data=data, message='You successfully registered new user!'), 200, {}
