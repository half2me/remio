import aiohttp
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
    } for k, v in request.app['io'].ports.items()])


async def getPortStatus(request: Request):
    port_id = int(request.match_info['id'])
    try:
        port = request.app['io'].ports[port_id]
        return web.json_response({
            'mode': port.mode,
            'level': port.level,
            'default_level': port.default
        })
    except KeyError:
        return web.HTTPNotFound()


async def addPort(request: Request):
    port_id = int(request.match_info['id'])
    request.app['io'].ports[port_id] = Port(app=request.app, number=port_id)
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
        if 'default_level' in j:
            port.default = j['default_level']
        return web.json_response({})
    except KeyError:
        return web.HTTPNotFound()


async def deletePort(request: Request):
    port_id = int(request.match_info['id'])
    try:
        del request.app['io'].ports[port_id]
        return web.json_response({})
    except KeyError:
        return web.HTTPNotFound()


async def ws_handler(request: Request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'][ws] = ws

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            pass
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    del request.app['websockets'][ws]

    return ws
