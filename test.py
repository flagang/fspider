from asyncio.coroutines import iscoroutine

import asyncio
import logging
from typing import AsyncIterable
from pydispatch import dispatcher

from fspider.engine import Crawler
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.spider import Spider

test_signal = object()


class TestSpider2(Spider):
    name = 'test2'
    settings = {
        'scheduler_cls': 'fspider.scheduler.PyScheduler',
        # 'scheduler_cls': 'fspider.scheduler.RedisScheduler',
        # 'redis_url': "redis://127.0.0.1:6379/11",
        'workers': 5
    }

    def __init__(self):
        super().__init__()
        dispatcher.connect(self.test, test_signal, sender=self)

    async def start_requests(self) -> AsyncIterable[Request]:
        yield Request(f'http://127.0.0.1:8000?index=8', callback=self.parse, dont_filter=True)

    async def parse(self, response: Response):
        self.logger.info(response.text)
        dispatcher.send(signal=test_signal, sender=self)
        yield

    def test(self):
        self.logger.info(f'test2 signal!!!!!!!!!')


class TestSpider(Spider):
    name = 'test'
    settings = {
        'scheduler_cls': 'fspider.scheduler.PyScheduler',
        # 'scheduler_cls': 'fspider.scheduler.RedisScheduler',
        # 'redis_url': "redis://127.0.0.1:6379/11",
        'workers': 5
    }

    def __init__(self):
        super().__init__()
        dispatcher.connect(self.test, test_signal, sender=self)

    async def start_requests(self) -> AsyncIterable[Request]:
        yield Request(f'http://127.0.0.1:8000?index=100', callback=self.parse, dont_filter=True)

    async def parse(self, response: Response):
        self.logger.info(response.text)
        dispatcher.send(signal=test_signal, sender=self)
        yield

    def test(self):
        self.logger.info(f'test signal!!!!!!!!!')


async def timer(crawler: Crawler):
    for i in range(1):
        await crawler.crawl(TestSpider)
        await asyncio.sleep(10)


async def serve(crawler: Crawler):
    from fastapi import FastAPI
    from uvicorn import Config, Server
    app = FastAPI()

    @app.get("/")
    async def hello(index: str):
        return {f"Hello: {index}"}

    config = Config(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
    server = Server(config)
    await server.serve()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s  [%(name)s] %(levelname)s: %(message)s')
    crawler = Crawler()
    # crawler.add_job(timer)#简易定时任务
    # crawler.add_job(serve)#同时启动web服务 请在py3.7使用,py3.8有bug
    crawler.add_spider(TestSpider)
    crawler.add_spider(TestSpider2)
    crawler.run(stop=False)
