import os

from cookie import AuthCookieFactory
from pysql import database_connect, print_ip
from snippet import get_snippet
from vial import render_template


def get_files(login=None):
    currDir = os.path.dirname(os.path.abspath(__file__))

    if (login != None):
        files = os.listdir(currDir + "/../serwer/usr/" + login)
    else:
        db, cursor = database_connect()
        cursor.execute("SELECT * FROM publicFiles")
        files = cursor.fetchall()

        db.close()
    return files


def save_file(login, fileName, privateFile):
    currDir = os.path.dirname(os.path.abspath(__file__))
    if (fileName == None):
        return False
    f = open(currDir + "/../serwer/usr/" + login + "/" + fileName, "w")
    f.write(privateFile.value)


def upload_file(headers, body, data):
    db, cursor = database_connect()
    token = str((AuthCookieFactory()).get_from_headers(headers).get_token())
    cursor.execute('''SELECT login FROM cookie WHERE token=%s''', token)
    login = str(cursor.fetchone()[0])

    save_file(login, data["upload"].filename, data["upload"])
    IP, time = print_ip(login)
    d_t, title, snippet = get_snippet(login)
    return render_template("mainpage.html", headers=headers, body=body, data=data, IP=IP, time=time, d_t=d_t,
                           title=title, snippets=snippet), 200, {}
