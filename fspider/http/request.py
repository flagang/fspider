import collections

from aiohttp import ClientTimeout
from typing import Callable, Dict, Any, AsyncGenerator, Union

from fspider.http.headers import Headers


class Request:
    def __init__(self, url: str, callback: Union[AsyncGenerator, Callable] = None, cookies: dict = None,
                 method: str = 'GET',
                 headers: Headers = None, dont_filter: bool = False, meta: dict = None, priority: int = 0,
                 data: Any = None, json: Any = None, timeout: int = None, **kwargs):
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
        self.url = url
        self.callback = callback
        self.headers = Headers(headers or {})
        self.json = json
        self.data = data
        self.method = method.upper()
        self.timeout = timeout
        self.kwargs = kwargs
        self.dont_filter = dont_filter
        self.priority = priority
        self.cookies = cookies
        if meta is None: meta = {}
        self.meta = meta

    def __str__(self):
        return f'<{self.url}>(referer:{self.headers.get("Referer", None)})'
