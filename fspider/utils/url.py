import weakref
from typing import Union
from urllib.parse import urlparse, ParseResult

from fspider.http.request import Request
from fspider.http.response import Response

_urlparse_cache = weakref.WeakKeyDictionary()


def urlparse_cached(r: Union[Request, Response]) -> ParseResult:
    if r not in _urlparse_cache:
        _urlparse_cache[r] = urlparse(r.url)
    return _urlparse_cache[r]
