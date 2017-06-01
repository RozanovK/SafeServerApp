from datetime import datetime
from pysql import database_connect


def get_snippet(headers, body, data, login):

    db, cursor = database_connect()
    snippet = str(data['snippet']) if 'snippet' in data else ''
    name = str(data['name']) if 'name' in data else ''

    name = name.replace('\t', '_')
    cursor.execute('''SELECT id FROM users WHERE login=%s''', login)
    id = int(cursor.fetchone()[0])
    f = '%Y-%m-%d %H:%M:%S'
    time = datetime.now().strftime(f)
    filename = '{0}.txt'.format(name)
    cursor.execute('''INSERT INTO snippets(id, datetime, path) VALUES(%s, %s, %s)''' % (id, time, filename))
    db.commit()
    db.close()

    file = open(filename, 'w')
    file.write(name)
    file.write(snippet)


def put_snippet(login):
    db, cursor = database_connect()



put_snippet('rozanovk')








