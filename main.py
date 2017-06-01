from vial import render_template, Vial
from pysql import auth, forgotPasswd, insertNewPass



def index(headers, body, data):
    return render_template('index.html', body=body, data=data), 200, {}

def recovery(headers, body, data):
    return render_template('recovery.html', body=body, data=data), 200, {}

routes = {
    '/': index,
    '/auth' : auth,
    '/recovery' : recovery,
    '/passwordRecovery' : forgotPasswd,
    '/insertNewPass': insertNewPass,
}

app = Vial(routes, prefix='/bach/drink', static='/static').wsgi_app()