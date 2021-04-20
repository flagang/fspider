import logging

from fspider import context
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.spidermiddlewares import SpiderMiddleware
from fspider.utils.type import SpiderResult

logger = logging.getLogger(__name__)


class DepthMiddleware(SpiderMiddleware):

    def __init__(self):
        super(DepthMiddleware, self).__init__()
        self.maxdepth = self.settings.get('DEPTH_LIMIT', 0)
        self.verbose_stats = self.settings.get('DEPTH_STATS_VERBOSE', False)
        self.prio = self.settings.get('DEPTH_PRIORITY', 0)

    async def process_spider_output(self, response: Response, result: SpiderResult) -> SpiderResult:
        spider = context.spider.get()
        response.meta.setdefault('depth', 0)
        async for r in result:
            if isinstance(r, Request):
                depth = response.meta['depth'] + 1
                r.meta['depth'] = depth
                if self.prio:
                    r.priority -= depth * self.prio
                logger.info(f'depth {r.meta["depth"]}')
                if self.maxdepth and depth > self.maxdepth:
                    logger.debug(
                        "Ignoring link (depth > %(maxdepth)d): %(requrl)s ",
                        {'maxdepth': self.maxdepth, 'requrl': r.url},
                        extra={'spider': spider}
                    )
                    continue
            yield r
