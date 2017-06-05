from auth import auth, forgot_password, insert_new_password, questions
from signup import signup_db
from vial import render_template, Vial


def index(headers, body, data):
    return render_template('index.html', body=body, data=data), 200, {}


def recovery(headers, body, data):
    question_tuple = questions()
    return render_template('recovery.html', body=body, data=data, questions = question_tuple), 200, {}

def signup(headers, body, data):
    question_tuple = questions()
    return render_template('signup.html', body=body, data=data, questions = question_tuple), 200, {}


routes = {
    '/': index,
    '/auth': auth,
    '/recovery': recovery,
    '/passwordRecovery': forgot_password,
    '/insert_new_password': insert_new_password,
    '/signup': signup,
    '/signup_db': signup_db
}

app = Vial(routes, prefix='', static='/static').wsgi_app()
