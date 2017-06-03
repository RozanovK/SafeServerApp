from pysql import database_connect, datetime_mysql
import pygments


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
    d_t = [number]
    title = [number]
    snippet = [number]
    cursor.execute('''SELECT datetime, title, snippet FROM snippets WHERE login = %s''', login)
    snippets = cursor.fetchall()
    for i in snippets:
        d_t[0], title[0], snippet[0] = i
    db.close()
    return d_t, title, snippet



get_snippet('rozanovk')








