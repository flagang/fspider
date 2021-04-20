from typing import AsyncIterable, Union, Dict, Optional

from fspider.http.request import Request

SpiderResult = AsyncIterable[Union[Request, Dict, None]]
MiddlewareSetting = Dict[str, Union[None, int]]
Item = Union[Dict]
