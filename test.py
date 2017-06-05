import hashlib

from pysql import database_connect, datetime_mysql


def put_snippet(login, title, snippet):
    db, cursor = database_connect()
    time = datetime_mysql()
    cursor.execute('''INSERT INTO snippets(login, datetime, title, snippet) VALUES(%s, %s, %s, %s)''',
                   (login, time, title, snippet))
    db.commit()
    db.close()


def insert_new_password(login, passwd, passwd_r):
    db, cursor = database_connect()
    pw = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
    if passwd == passwd_r:
        cursor.execute('''UPDATE users SET password= %s WHERE login= %s''', (pw, login))
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False

#put_snippet('rozanovk', 'My second snippet!', 'def put_snippet(login, title, snippet):\
#    \ndb, cursor = database_connect()\
#   \ntime = datetime_mysql()\
#    \ncursor.execute(''\'INSERT INTO snippets(login, datetime, title, snippet) VALUES(%s, %s, %s, %s)''\' , (login, time, title, snippet))\
#   \ndb.commit()\
#   \ndb.close()')

# print(create_token())


insert_new_password('rozanovk', 'kaczuszki', 'kaczuszki')
