import logging
from http.cookies import SimpleCookie
from aiohttp import ClientSession, ClientTimeout
from fspider.http.request import Request
from fspider.http.response import Response

logger = logging.getLogger(__name__)


class Client:
    session: ClientSession = None

    def __init__(self, *args, **kwargs):
        self.session = ClientSession(*args, **kwargs)

    async def down(self, request: Request) -> Response:
        logging.info(f'begin down {request}')
        if request.method == "GET":
            return await self.get(request)
        else:
            return await self.post(request)

    async def get(self, request: Request) -> Response:
        async with self.session.get(url=request.url, headers=request.headers,
                                    timeout=ClientTimeout(total=request.timeout),
                                    **request.kwargs) as r:
            body = await r.read()
            return Response(request.url, cookies=self.extract_cookies(r.cookies), body=body, status=r.status,
                            encoding=r.get_encoding(), client_response=r,
                            meta=request.meta)

    async def post(self, request: Request) -> Response:
        async with self.session.post(url=request.url, json=request.json, data=request.data, headers=request.headers,
                                     timeout=ClientTimeout(total=request.timeout), **request.kwargs) as r:
            body = await r.read()
            return Response(request.url, cookies=self.extract_cookies(r.cookies), body=body, status=r.status,
                            encoding=r.get_encoding(), client_response=r,
                            meta=request.meta)

    def extract_cookies(self, cookies: SimpleCookie) -> dict:
        return {k: v.value for k, v in cookies.items()}

    async def close(self):
        logger.info('client session closed')
        await self.session.close()
