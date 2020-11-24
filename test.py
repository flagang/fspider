from asyncio.coroutines import iscoroutine

import asyncio

import logging

from typing import AsyncIterable

from fspider.engine import Crawler
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.spider import Spider


class TestSpider(Spider):
    name = 'test'
    settings = {
        'scheduler_cls': 'fspider.scheduler.RedisScheduler',
        'redis_url': "redis://172.16.22.74:6379/11",
        'workers': 5
    }

    async def start_requests(self) -> AsyncIterable[Request]:
        for i in range(10):
            yield Request('http://127.0.0.1:8000', callback=self.parse, dont_filter=True)

    async def parse(self, response: Response):
        print(response.text)
        yield


async def timer(crawler: Crawler):
    for i in range(10):
        await crawler.crawl(TestSpider)
        await asyncio.sleep(10)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    crawler = Crawler()
    crawler.add_job(timer)
    crawler.add_spider(TestSpider)
    crawler.run(stop=False)
