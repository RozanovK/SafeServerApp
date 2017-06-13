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
    if not check_title(title):
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
    return render_template('mainpage.html', headers=headers, body=body, data=data, IP=IP, time=time), 200, {}




def redirect_main(headers, body, data, login):
    IP, time = pysql.print_ip(login)
    return render_template('mainpage.html', headers=headers, body=body, data=data, IP=IP, time=time), 200, {}


def get_all_snipets():
    db, cursor = pysql.database_connect()
    cursor.execute('SELECT datetime, title, snippet FROM snippets')
    snippets = cursor.fetchall()
    # d_t, title, snippet = zip(*snippets)
    db.close()
    return snippets


def check_title(title):
    title = title.split()
    for word in title:
        for i in word:
            if not i.isalpha() or i.isdigit():
                return False
    return True
