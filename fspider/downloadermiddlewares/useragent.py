import logging
from typing import Union

from fspider.downloadermiddlewares import DownloaderMiddleware
from fspider.http.request import Request
from fspider.http.response import Response

logger = logging.getLogger(__name__)


class UserAgentMiddleware(DownloaderMiddleware):
    def __init__(self):
        super(UserAgentMiddleware, self).__init__()
        self.user_agent = self.settings.get('USER_AGENT')

    async def process_request(self, request: Request) -> Union[Request, Response, None]:
        if self.user_agent:
            request.headers.setdefault('User-Agent', self.user_agent)
