import logging

from fspider.http.response import Response
from fspider.utils.middleware import MiddlewareLoader, Middleware
from fspider.utils.type import SpiderResult

logger = logging.getLogger(__name__)


class SpiderMiddleware(Middleware):
    async def process_start_requests(self, result: SpiderResult) -> SpiderResult:
        async for r in result:
            yield r

    async def process_spider_exception(self, response: Response, exception: Exception):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_spider_input(self, response: Response):
        return None

    async def process_spider_output(self, response: Response, result: SpiderResult) -> SpiderResult:
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        async for i in result:
            yield i


class SpiderMiddlewareManager(MiddlewareLoader):
    name = 'SPIDER_MIDDLEWARES'

    async def process_start_requests(self, result: SpiderResult) -> SpiderResult:
        for md in self._middlewares:
            result = md.process_start_requests(result)
        async for r in result:
            yield r

    async def process_spider_output(self, response: Response, result: SpiderResult) -> SpiderResult:
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for md in self._middlewares:
            result = md.process_spider_output(response, result)
        async for r in result:
            yield r
