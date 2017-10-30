from aiohttp import web

from gpio import Io
from routes import setup_routes
from views import setup_view

app = web.Application()
setup_routes(app)
setup_view(app)

app['io'] = Io()
app.on_startup.append(app['io'].onStartup)
app.on_shutdown.append(app['io'].onShutdown)
web.run_app(app, host='0.0.0.0')
