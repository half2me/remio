from views import *


def setup_routes(app):
    app.router.add_get('/', home)
    app.router.add_get('/ports', listPorts)
    app.router.add_get('/ports/{id}', getPortStatus)
    app.router.add_put('/ports/{id}', addPort)
    app.router.add_post('/ports/{id}', setPortStatus)

    app.router.add_static('/', path='static', name='static')