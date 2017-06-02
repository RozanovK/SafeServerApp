from datetime import datetime
from pysql import database_connect, datetime_mysql


TEMPLATE = 'mainpage.html'


def put_snippet(headers, body, data, login):
    db, cursor = database_connect()
    time = datetime_mysql()
    snippet = str(data['snippet']) if 'snippet' in data else ''
    title = str(data['title']) if 'title' in data else ''
    cursor.execute('''INSERT INTO snippets(login, datetime, title, snippet) VALUES(%s, %s, %s)''' , (login, time, title, snippet))
    db.commit()
    db.close()


def get_snippet(login):
    db, cursor = database_connect()
    cursor.execute('''SELECT COUNT(*) FROM snippets WHERE login = %s''', login)
    number = int(cursor.fetchone()[0])
    cursor.execute('''SELECT datetime, title, path FROM snippets WHERE login = %s''', login)
    snippets = cursor.fetchall()
    db.close()
    return snippets




put_snippet('rozanovk')








