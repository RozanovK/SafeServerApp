from vial import render_template, Vial
from pysql import auth



def index(headers, body, data):
    return render_template('index.html', body=body, data=data), 200, {}

routes = {
    '/': index,
    '/auth' : auth,
}

app = Vial(routes, prefix='/bach/drink', static='/static').wsgi_app()