from unidecode import unidecode

import pysql
from cookie import AuthCookieFactory
from vial import render_template


def put_snippet(headers, body, data):
    db, cursor = pysql.database_connect()
    time = pysql.datetime_mysql()
    snippet = str(data['snippet']) if 'snippet' in data else ''
    title = str(data['title']) if 'title' in data else ''
    snippet = unidecode(snippet)  # decode non-standard letters
    if not check_title():
        return render_template('new_snippet.html', headers=headers, body=body, data=data,
                               message='Title can only contain letters or digits!'), 200, {}
    if len(title) > 40:
        return render_template('new_snippet.html', headers=headers, body=body, data=data,
                               message='Title is too long!'), 200, {}
    if len(snippet) > 1000:
        return render_template('new_snippet.html', headers=headers, body=body, data=data,
                               message='Snippet is too long!'), 200, {}
    token = str((AuthCookieFactory()).get_from_headers(headers).get_token())
    cursor.execute('''SELECT login FROM cookie WHERE token=%s''', token)
    login = str(cursor.fetchone()[0])
    cursor.execute('''INSERT INTO snippets(login, datetime, title, snippet) VALUES(%s, %s, %s, %s)''',
                   (login, time, title, snippet))
    db.commit()
    db.close()
    IP, time = pysql.print_ip(login)
    d_t, titles, snippets = get_snippet(login)
    return render_template('mainpage.html', headers=headers, body=body, data=data, IP=IP, time=time, d_t=d_t,
                           title=titles, snippets=snippets), 200, {}


def get_snippet(login):
    db, cursor = pysql.database_connect()
    cursor.execute('''SELECT COUNT(*) FROM snippets WHERE login = %s''', (login))
    number = int(cursor.fetchone()[0])
    d_t = [number]
    title = [number]
    snippet = [number]
    cursor.execute('''SELECT datetime, title, snippet FROM snippets WHERE login = %s''', (login))
    snippets = cursor.fetchall()
    for i in snippets:
        d_t[0], title[0], snippet[0] = i
    db.close()
    return d_t, title, snippet


def redirect_main(headers, body, data, login):
    IP, time = pysql.print_ip(login)
    d_t, title, snippet = get_snippet(login)
    return render_template('mainpage.html', headers=headers, body=body, data=data, IP=IP, time=time, d_t=d_t,
                           title=title, snippets=snippet), 200, {}


def get_all_snipets():
    db, cursor = pysql.database_connect()
    cursor.execute('SELECT COUNT(*) FROM snippets')
    number = int(cursor.fetchone()[0])
    d_t = [number]
    title = [number]
    snippet = [number]
    cursor.execute('SELECT datetime, title, snippet FROM snippets')
    snippets = cursor.fetchall()
    for i in snippets:
        d_t[0], title[0], snippet[0] = i
    db.close()
    return d_t, title, snippet


def check_title(title):
    title = title.split()
    for word in title:
        for i in word:
            if not i.isalpha() or i.isdigit():
                return False
    return True
