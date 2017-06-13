import os

from cookie import AuthCookieFactory
from pysql import database_connect, print_ip
from vial import render_template


def upload_file(headers, body, data):
    db, cursor = database_connect()
    token = str((AuthCookieFactory()).get_from_headers(headers).get_token())
    cursor.execute('''SELECT login FROM cookie WHERE token=%s''', token)
    x = cursor.fetchone()
    if x is None:
        return render_template('unauthorised_request.html', headers=headers, body=body, data=data,
                               message='Unauthorised try to log in!'), 200, {}
    login = str(x[0])
    file_name = data['upload'].filename if 'upload' in data else ''
    if body != '' and file_name != '':
        currDir = os.path.dirname(os.path.abspath(__file__))
        filepath = currDir + "/../serwer/usr/" + login + "/" + file_name
        with open(filepath, "wb") as f:
            f.write(data['upload'].value)
            f.close()
        cursor.execute('INSERT INTO files(login, file) VALUES (%s, %s)', (login, file_name))
        db.commit().close()
        IP, time = print_ip(login)
        return render_template("mainpage.html", headers=headers, body=body, data=data, IP=IP, time=time,
                               message='Your file has been successfully uploaded'), 200, {}

    return render_template('upload.html', headers=headers, body=body, data=data), 200, {}
