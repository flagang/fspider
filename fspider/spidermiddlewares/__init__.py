import logging
from typing import Dict, List

from fspider import context
from fspider.http.response import Response
from fspider.utils.middleware import loads
from fspider.utils.type import SpiderRequest, SpiderResults, MiddlewareSetting

logger = logging.getLogger(__name__)


class SpiderMiddleware:
    async def process_start_requests(self, result: SpiderRequest) -> SpiderRequest:
        async for r in result:
            yield r

    async def process_spider_exception(self, response: Response, exception: Exception):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_spider_input(self, response: Response):
        return None

    async def process_spider_output(self, response: Response, result: SpiderRequest) -> SpiderRequest:
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        async for i in result:
            yield i


class SpiderMiddlewareManager:
    name = 'SPIDER_MIDDLEWARES'

    def __init__(self, settings: Dict = None):
        if settings is None:
            settings = context.settings.get()
        logger.info(settings.get(self.name))
        self._middlewares: List[SpiderMiddleware] = loads(settings.get(self.name))
        logger.info(self._middlewares)

    async def process_start_requests(self, result: SpiderRequest) -> SpiderRequest:
        for md in self._middlewares:
            result = md.process_start_requests(result)
        async for r in result:
            yield r

    async def process_spider_output(self, response: Response, result: SpiderRequest) -> SpiderRequest:
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for md in self._middlewares:
            result = md.process_spider_output(response,result)
        async for r in result:
            yield r
