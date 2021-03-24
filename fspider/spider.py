from typing import Generator, List, Dict, Iterable, AsyncIterable, Optional
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.utils.misc import load_object


class Spider:
    settings: Dict = {
        'scheduler_cls': 'fspider.scheduler.RedisScheduler'
    }
    start_urls: List[str]
    name: Optional[str] = None

    def __init__(self):
        scheduler_cls = self.settings['scheduler_cls']
        self._scheduler = load_object(scheduler_cls)(self)

    @classmethod
    async def create_spider(cls) -> "Spider":
        obj = cls()
        await obj.spider_opened()
        return obj

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
        pass

    async def spider_closed(self):
        print('spider_closed ')
        pass
