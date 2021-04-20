import logging
from typing import Union

from fspider.http.request import Request
from fspider.http.response import Response
from fspider.utils.middleware import MiddlewareLoader, Middleware

logger = logging.getLogger(__name__)


class DownloaderMiddleware(Middleware):
    async def process_request(self, request: Request) -> Union[Request, Response, None]:
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    async def process_response(self, request: Request, response: Response) -> Union[Request, Response]:
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    async def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass


class DownloaderMiddlewareManager(MiddlewareLoader):
    name = 'DOWNLOADER_MIDDLEWARES'

    async def down(self, request: Request) -> Union[Request, Response, None]:
        for md in self._middlewares:
            result = await md.process_request(request)
            if result is not None:
                break
        if isinstance(result, Response):
            for md in reversed(self._middlewares):
                result = await md.process_response(request, result)
                if not isinstance(result, Response):
                    break
        return result
