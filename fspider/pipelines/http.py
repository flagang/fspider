from aiohttp import ClientSession, TCPConnector

from fspider import signals

from fspider.pipelines import Pipeline
from fspider.signals import spider_opened, spider_closed


class HttpClient:
    CONN_LIMIT = 20
    LIMIT_PER_HOST = 5

    def __init__(self):
        super().__init__()
        signals.connect(receiver=self.spider_opened, signal=signals.spider_opened)
        signals.connect(receiver=self.spider_opened, signal=signals.spider_opened)
        self.session: ClientSession = ClientSession(
            connector=TCPConnector(limit=self.CONN_LIMIT, limit_per_host=self.LIMIT_PER_HOST))

    async def spider_closed(self):
        await self.session.close()

    async def spider_opened(self):
        pass
