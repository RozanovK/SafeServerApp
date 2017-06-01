from vial import render_template, Vial
from pysql import auth, forgot_password, insert_new_password


def index(headers, body, data):
    return render_template('index.html', body=body, data=data), 200, {}


def recovery(headers, body, data):
    return render_template('recovery.html', body=body, data=data), 200, {}


routes = {
    '/': index,
    '/auth': auth,
    '/recovery': recovery,
    '/passwordRecovery': forgot_password,
    '/insert_new_password': insert_new_password,
}

app = Vial(routes, prefix='/bach/drink', static='/static').wsgi_app()
