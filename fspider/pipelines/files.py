import asyncio
import hashlib
import mimetypes
import os
import typing
from typing import Optional

from aiohttp import ClientTimeout

from fspider.http.request import Request
from fspider.pipelines import Pipeline
from fspider.pipelines.http import HttpClient
from fspider.utils.type import Item


class MediaPipeline(Pipeline, HttpClient):
    """
    并发下载视频、图片等
    """
    meida_key = ''
    CONN_LIMIT = 5
    LIMIT_PER_HOST = 3
    file_dir = ''
    size_limit = 1024 * 1024 * 1024  # 1g
    time_limit = 10 * 60  # 10分钟

    async def process_item(self, item: Item) -> Optional[Item]:
        urls = item.get(self.meida_key, [])
        results = await self.downloads(urls)
        item = await self.item_completed(results, item)
        return item

    async def item_completed(self, results: typing.Union[str, Exception], item: Item) -> Item:
        raise NotImplemented

    def from_urls(self, urls: list[str]) -> typing.Iterable[Request]:
        for url in urls:
            yield Request(url)

    async def downloads(self, urls):
        results = await asyncio.gather(*[self.down(url) for url in urls], return_exceptions=True)
        return results

    def get_filepath(self, url: str, content_type: str):
        media_id = hashlib.md5(url.encode('utf8')).hexdigest()
        ext = self.guess_extension(url, content_type)
        return os.path.join(self.file_dir, f'{media_id}{ext}')

    async def down(self, url: str) -> str:
        timeout = None
        if self.time_limit > 0:
            timeout = ClientTimeout(total=self.time_limit)
        async with self.session.get(url, timeout=timeout) as resp:
            if self.size_limit:
                _size = resp.headers.get('Content-Length', 0)
                if _size > 0 and _size > self.size_limit:
                    raise Exception('size_limit')
            filepath = self.get_filepath(url, resp.headers.get('Content-Type', ''))
            with open(filepath, mode='wb') as f:
                async for data in resp.content.iter_chunked(1024):
                    f.write(data)
            return filepath

    @staticmethod
    def guess_extension(url: str, content_type: str = '') -> str:
        if media_ext := mimetypes.guess_extension(content_type):
            return media_ext
        media_ext = os.path.splitext(url)[1]
        if media_ext not in mimetypes.types_map:
            media_type = mimetypes.guess_type(url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        return media_ext
