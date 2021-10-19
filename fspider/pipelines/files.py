import asyncio
import hashlib
import logging
import mimetypes
import os
import time
import typing
from typing import Optional

from aiohttp import ClientTimeout

from fspider.http.request import Request
from fspider.pipelines import Pipeline
from fspider.pipelines.http import HttpClient
from fspider.utils.asynclib import aenumerate
from fspider.utils.type import Item

logger = logging.getLogger(__name__)


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

    def from_urls(self, urls: typing.List[str]) -> typing.Iterator[Request]:
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
        logger.debug(f'start down {url}')
        async with self.session.get(url, timeout=timeout) as resp:
            if self.size_limit:
                _size = resp.headers.get('Content-Length', 0)
                _size = int(_size)
                if _size > 0 and _size > self.size_limit:
                    raise Exception('size_limit')
            filepath = self.get_filepath(url, resp.headers.get('Content-Type', ''))
            _start_time = time.time()
            with open(filepath, mode='wb') as f:
                async for index, data in aenumerate(resp.content.iter_chunked(1024), 1):
                    if index == 50 and _size > 0 and self.time_limit > 0:  # 50kb
                        speed = 50 / (time.time() - _start_time)
                        _ttime = _size / 1024 / speed
                        logger.debug(f'文件大小:{(_size/1024**2):.2f}M speed:{speed:.2f} kb/s 预计时间:{_ttime:.2f}  {url}')
                        if _ttime > self.time_limit:
                            logger.info(f'预计时间:{_ttime:.2f} > {self.time_limit}  {url}')
                            raise Exception('time limit')
                    f.write(data)
            logger.debug(f'end down {url}')
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
