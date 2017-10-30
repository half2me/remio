from aiohttp import web
from aiohttp.web import Request, Application, HTTPFound

from gpio import Port


def setup_view(app: Application):
    pass


async def homePage(request: Request):
    return HTTPFound('/main.html')


async def listPorts(request: Request):
    return web.json_response([{
        'id': k,
        'mode': v.mode,
        'level': v.level,
    } for k, v in request.app['io'].ports.items()])


async def getPortStatus(request: Request):
    port_id = int(request.match_info['id'])
    try:
        port = request.app['io'].ports[port_id]
        return web.json_response({
            'mode': port.mode,
            'level': port.level,
        })
    except KeyError:
        return web.HTTPNotFound()


async def addPort(request: Request):
    port_id = int(request.match_info['id'])
    request.app['io'].ports[port_id] = Port(port_id)
    return web.json_response({})


async def setPortStatus(request: Request):
    port_id = int(request.match_info['id'])
    try:
        port = request.app['io'].ports[port_id]
        j = await request.json()
        if 'mode' in j:
            port.mode = j['mode']
        if 'level' in j:
            port.level = j['level']
        return web.json_response({})
    except KeyError:
        return web.HTTPNotFound()
