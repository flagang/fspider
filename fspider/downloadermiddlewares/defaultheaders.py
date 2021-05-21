from typing import Union

from fspider.downloadermiddlewares import DownloaderMiddleware
from fspider.http.request import Request
from fspider.http.response import Response

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,en;q=0.7,la;q=0.6,ja;q=0.5',
    'accept-encoding': 'gzip, deflate, br',
}


class DefaultHeadersMiddleware(DownloaderMiddleware):

    def __init__(self):
        super(DefaultHeadersMiddleware, self).__init__()
        self._headers = self.settings.get('DEFAULT_REQUEST_HEADERS', DEFAULT_REQUEST_HEADERS)

    async def process_request(self, request: Request) -> Union[Request, Response, None]:
        for k, v in self._headers.items():
            request.headers.setdefault(k, v)
