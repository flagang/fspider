import logging
from typing import Generator, List, Dict, Iterable, AsyncIterable, Optional

from fspider import signals
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.utils.misc import load_object
from fspider.utils.project import get_settings


class Spider:
    name = 'fspider'
    custom_settings: Dict = {
        'scheduler_cls': 'fspider.scheduler.RedisScheduler'
    }
    start_urls: List[str]
    name: Optional[str] = None
    allow_domains = []

    def __init__(self):
        self.settings = get_settings()
        self.settings.update(self.custom_settings)
        scheduler_cls = self.settings['scheduler_cls']
        self._scheduler = load_object(scheduler_cls)(self)
        signals.connect(receiver=self.spider_opened, sender=self, signal=signals.spider_opened)
        signals.connect(receiver=self.spider_closed, sender=self, signal=signals.spider_closed)
        self.logger = logging.getLogger(self.name)

    async def start_requests(self) -> AsyncIterable[Request]:
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response: Response):
        raise NotImplemented

    @classmethod
    def start(cls):
        from fspider.engine import start_spider
        start_spider(cls)

    async def spider_opened(self):
        self.logger.info('spider_opened!!!!!!!!!!!')

    async def spider_closed(self):
        self.logger.info('spider_closed ')
        pass
