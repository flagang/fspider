import logging

from aiohttp import ClientSession, TCPConnector

from fspider import signals
from fspider.http.request import Request
from fspider.http.response import Response

session: ClientSession = None


async def down(request: Request) -> Response:
    logging.info(f'begin down {request}')
    global session
    if session is None:
        session = ClientSession(connector=TCPConnector(limit=200))
        signals.connect(close, signals.crawler_closed, sender='fspider')
    if request.method == "GET":
        return await get(request)
    else:
        return await post(request)


async def get(request: Request) -> Response:
    async with session.get(url=request.url, headers=request.headers, timeout=request.client_timeout,
                           **request.kwargs) as r:
        body = await r.read()
        return Response(request.url, body=body, status=r.status, encoding=r.get_encoding(), meta=request.meta)


async def post(request: Request) -> Response:
    async with session.post(url=request.url, json=request.json, data=request.data, headers=request.headers,
                            timeout=request.client_timeout, **request.kwargs) as r:
        body = await r.read()
        return Response(request.url, body=body, status=r.status, encoding=r.get_encoding(), meta=request.meta)


async def close():
    await session.close()
