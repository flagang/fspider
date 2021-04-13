from typing import AsyncIterable, Union, Dict

from fspider.http.request import Request

SpiderResults = AsyncIterable[Union[Request, Dict]]
SpiderRequest = AsyncIterable[Request]
MiddlewareSetting = Dict[str, Union[None, int]]