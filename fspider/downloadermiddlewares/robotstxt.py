import logging
from asyncio import Event
from typing import Union
from urllib.robotparser import RobotFileParser

from fspider import context
from fspider.downloadermiddlewares import DownloaderMiddleware
from fspider.exceptions import IgnoreRequest, NotConfigured
from fspider.http.downloader import down
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.utils.url import urlparse_cached

logger = logging.getLogger(__name__)
ROBOTS_NOT_FOUND = object()


class RobotsTxtMiddleware(DownloaderMiddleware):
    _parsers = {}  # 所有爬虫公用

    def __init__(self):
        super(RobotsTxtMiddleware, self).__init__()
        if not self.settings.get('ROBOTSTXT_OBEY'):
            raise NotConfigured
        self.robots_user_agent = self.settings.get('ROBOTSTXT_USER_AGENT')
        self.user_agent = self.settings.get('USER_AGENT')

    async def process_request(self, request: Request) -> Union[Request, Response, None]:
        if request.meta.get('dont_obey_robotstxt'):
            return
        url = urlparse_cached(request)
        netloc = url.netloc
        if netloc not in self._parsers:
            robotsurl = f"{url.scheme}://{url.netloc}/robots.txt"
            robots_request = Request(robotsurl)
            _event = Event()
            try:  # 并发访问时候 通过_event 防止重复请求robots
                self._parsers[netloc] = _event
                resp = await down(robots_request)
                if resp.status == 404:
                    self._parsers[netloc] = ROBOTS_NOT_FOUND
                else:
                    _parser = RobotFileParser()
                    _parser.parse(resp.text.splitlines())
                    self._parsers[netloc] = _parser
            finally:
                _event.set()
        _parser = self._parsers[netloc]
        if _parser is ROBOTS_NOT_FOUND:
            return
        if isinstance(_parser, Event):
            await _parser.wait()
            return await self.process_request(request)
        else:
            user_agent = self.robots_user_agent or request.headers.get('uset-agent', self.user_agent)
            if not _parser.can_fetch(user_agent, request.url):
                logger.info("Forbidden by robots.txt: %(request)s",
                            {'request': request}, extra={'spider': context.spider.get()})
                raise IgnoreRequest("Forbidden by robots.txt")
