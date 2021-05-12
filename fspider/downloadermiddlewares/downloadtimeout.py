from typing import Union

from aiohttp import ClientTimeout

from fspider.downloadermiddlewares import DownloaderMiddleware
from fspider.http.request import Request
from fspider.http.response import Response


class DownloadTimeoutMiddleware(DownloaderMiddleware):

    def __init__(self):
        super(DownloadTimeoutMiddleware, self).__init__()
        self._timeout = self.settings.get('DOWNLOAD_TIMEOUT', 60)

    async def process_request(self, request: Request) -> Union[Request, Response, None]:
        if not request.timeout:
            request.timeout = self._timeout
