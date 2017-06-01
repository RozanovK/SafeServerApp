from datetime import datetime
from pysql import database_connect
from tempfile import TemporaryFile


def get_snippet(headers, body, data, login):

    db, cursor = database_connect()
    snippet = str(data['snippet']) if 'snippet' in data else ''
    name = str(data['name']) if 'name' in data else ''

    name = name.replace(' ', '_')
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.now().strftime(f)
    filename = '{0}.txt'.format(name)
    cursor.execute('''INSERT INTO snippets(login, datetime, path) VALUES(%s, %s, %s)''' , (login, time, filename))
    db.commit()
    db.close()

    file = open(filename, 'w')
    file.write('{0}\n'.format(name))
    file.write(snippet)
    file.close()


def put_snippet(login):
    db, cursor = database_connect()
    cursor.execute('''SELECT COUNT(*) FROM snippets WHERE login = %s''', login)
    number = int(cursor.fetchone()[0])
    cursor.execute('''SELECT datetime, path FROM snippets WHERE login = %s''', login)
    snippets = cursor.fetchall()
    print (snippets)




put_snippet('rozanovk')








