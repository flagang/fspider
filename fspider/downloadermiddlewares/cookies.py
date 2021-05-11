import logging
from collections import defaultdict
from typing import Union
from fspider.downloadermiddlewares import DownloaderMiddleware
from fspider.exceptions import NotConfigured
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.utils.url import urlparse_cached

logger = logging.getLogger(__name__)


class CookiesMiddleware(DownloaderMiddleware):
    def __init__(self):
        super(CookiesMiddleware, self).__init__()
        if not self.settings.get('COOKIES_ENABLED', True):
            raise NotConfigured
        self._jars = defaultdict(dict)

    async def process_request(self, request: Request) -> Union[Request, Response, None]:
        if request.meta.get('dont_merge_cookies', False):
            return
        ck = request.meta.get('cookiejar') or urlparse_cached(request).hostname
        jar = self._jars[ck]
        req_cookie = request.cookies
        if req_cookie:
            jar.update(req_cookie)
        request.headers['cookie'] = ';'.join([f'{k}={v}' for k, v in jar.items()])
        logger.info(request.headers['cookie'])

    async def process_response(self, request: Request, response: Response) -> Union[Request, Response]:
        if request.meta.get('dont_merge_cookies', False):
            return response
        ck = request.meta.get('cookiejar') or urlparse_cached(request).hostname
        jar = self._jars[ck]
        jar.update(response.cookies or {})
        return response
