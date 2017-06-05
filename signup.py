from pysql import database_connect
import hashlib
from vial import render_template

def signup_db(headers, body, data):
    db, cursor = database_connect()
    login = str(data['name']) if 'name' in data else ''
    answer = str(data['answer']) if 'answer' in data else ''
    passwd = str(data['pw']) if 'pw' in data else ''

    password = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    answer = hashlib.sha256(answer.encode('utf-8')).hexdigest()
    cursor.execute('''INSERT INTO users (login, password, answer) VALUES (%s, %s, %s)''', (login, password, answer))
    db.commit()
    db.close()
    return render_template('index.html', body=body, data=data), 200, {}

