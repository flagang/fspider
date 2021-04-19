from typing import AsyncIterable, Dict
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.spider import Spider


class TestSpider(Spider):
    name = 'test'
    custom_settings: Dict = {
        'scheduler_cls': 'fspider.scheduler.PyScheduler'
    }

    def __init__(self):
        super().__init__()

    async def start_requests(self) -> AsyncIterable[Request]:
        for i in range(10):
            yield Request(f'http://127.0.0.1:8000?index={i}', callback=self.parse, dont_filter=True)

    async def parse(self, response: Response):
        self.logger.info(response.text)
        yield {'index': response.text}

    async def spider_opened(self):
        await super(TestSpider, self).spider_opened()
