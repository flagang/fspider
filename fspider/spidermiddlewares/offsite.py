import logging
from urllib.parse import urlparse

from fspider import  context
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.spider import Spider
from fspider.spidermiddlewares import SpiderMiddleware
from fspider.utils.type import SpiderResult

logger = logging.getLogger(__name__)


class OffsiteMiddleware(SpiderMiddleware):
    def __init__(self):
        super(OffsiteMiddleware, self).__init__()
        self.spider: Spider = context.spider.get()
        self.domains_seen = set()

    async def process_spider_output(self, response: Response, result: SpiderResult) -> SpiderResult:
        async for r in result:
            if isinstance(r, Request):
                if r.dont_filter or self.should_follow(r):
                    yield r
                else:
                    domain = urlparse(r.url).hostname
                    if domain and domain not in self.domains_seen:
                        self.domains_seen.add(domain)
                        logger.debug(
                            "Filtered offsite request to %(domain)r: %(request)s",
                            {'domain': domain, 'request': r}, extra={'spider': self.spider})
            else:
                yield r

    def should_follow(self, request: Request):
        host = urlparse(request.url).hostname or ''
        if not self.spider.allow_domains:
            return True
        for domain in self.spider.allow_domains:
            if domain != host or not host.endswith(f'.{domain}'):
                return False
        return True
