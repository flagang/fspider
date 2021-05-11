import collections

from aiohttp import ClientTimeout
from typing import Callable, Dict, Any, AsyncGenerator, Union


class Request:
    def __init__(self, url: str, callback: Union[AsyncGenerator, Callable], cookies: dict = None, method: str = 'GET',
                 headers: Dict = None, dont_filter: bool = False, meta: dict = None, priority: int = 0,
                 data: Any = None, json: Any = None, timeout: int = 10, **kwargs):
        """

        :param url:
        :param callback:
        :param method:
        :param headers:
        :param dont_filter:
        :param data:
        :param json:
        :param timeout:
        :param kwargs:
        """
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
        self.url = url
        self.callback = callback
        if headers:
            self.headers.update(headers)
        self.json = json
        self.data = data
        self.method = method.upper()
        self.timeout = timeout
        self.client_timeout = ClientTimeout(connect=timeout)
        self.kwargs = kwargs
        self.dont_filter = dont_filter
        self.priority = priority
        self.cookies = cookies
        if meta is None: meta = {}
        self.meta = meta

    def __str__(self):
        return f'<{self.url}>(referer:{self.headers.get("Referer", None)})'
