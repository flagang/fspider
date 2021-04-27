from typing import Union
from fspider.downloadermiddlewares import DownloaderMiddleware
from fspider.http.downloader import down
from fspider.http.request import Request
from fspider.http.response import Response


class DefaultDownloaderMiddleware(DownloaderMiddleware):
    async def process_request(self, request: Request) -> Union[Request, Response, None]:
        response = await down(request)
        response.request = request
        return response
