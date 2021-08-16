import logging
from http.cookies import SimpleCookie

from aiohttp import ClientSession, TCPConnector, ClientTimeout

from fspider import signals
from fspider.http.request import Request
from fspider.http.response import Response

logger = logging.getLogger(__name__)
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
    async with session.get(url=request.url, headers=request.headers, timeout=ClientTimeout(total=request.timeout),
                           **request.kwargs) as r:
        body = await r.read()
        return Response(request.url, cookies=extract_cookies(r.cookies), body=body, status=r.status,
                        encoding=r.get_encoding(), client_response=r,
                        meta=request.meta)


async def post(request: Request) -> Response:
    async with session.post(url=request.url, json=request.json, data=request.data, headers=request.headers,
                            timeout=ClientTimeout(total=request.timeout), **request.kwargs) as r:
        body = await r.read()
        return Response(request.url, cookies=extract_cookies(r.cookies), body=body, status=r.status,
                        encoding=r.get_encoding(), client_response=r,
                        meta=request.meta)


def extract_cookies(cookies: SimpleCookie) -> dict:
    return {k: v.value for k, v in cookies.items()}


async def close():
    logger.info('client session closed')
    await session.close()
