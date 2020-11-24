from typing import AsyncIterable

from fspider.http.request import Request
from fspider.spider import Spider


class SpiderMiddleware:
    async def process_start_urls(self, result: AsyncIterable[Request], spider: Spider) -> AsyncIterable[Request]:
        pass


