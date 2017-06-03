from pysql import database_connect, datetime_mysql


def put_snippet(login, title, snippet):
    db, cursor = database_connect()
    time = datetime_mysql()
    cursor.execute('''INSERT INTO snippets(login, datetime, title, snippet) VALUES(%s, %s, %s, %s)''',
                   (login, time, title, snippet))
    db.commit()
    db.close()


put_snippet('rozanovk', 'My second snippet!', 'def put_snippet(login, title, snippet):\
    \ndb, cursor = database_connect()\
    \ntime = datetime_mysql()\
    \ncursor.execute(''\'INSERT INTO snippets(login, datetime, title, snippet) VALUES(%s, %s, %s, %s)''\' , (login, time, title, snippet))\
    \ndb.commit()\
    \ndb.close()')
