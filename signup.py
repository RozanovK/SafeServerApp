from pysql import database_connect
from main import index
import hashlib

def signup_db(headers, body, data):
    db, cursor = database_connect()
    login = str(data['name']) if 'name' in data else ''
    passwd = str(data['Password']) if 'Password' in data else ''
    answer = str(data['answer']) if 'answer' in data else ''

    password = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    answer = hashlib.sha256(answer.encode('utf-8')).hexdigest()
    cursor.execute('''INSERT INTO users (login, password, answer) VALUES (%s, %s, %s)''', (login, password, answer))
    db.commit()
    db.close()
    index()
