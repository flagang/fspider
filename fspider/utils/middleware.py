import logging
from typing import Dict, Union, List

from fspider import context
from fspider.utils.misc import load_object
from fspider.utils.type import MiddlewareSetting

logger = logging.getLogger(__name__)


def loads(mw_settings: MiddlewareSetting) -> List:
    _middlewares = []
    mwlist = {k: v for k, v in mw_settings.items() if v is not None}
    mw_paths: List[str] = sorted(mwlist, key=mwlist.get)
    for mw_path in mw_paths:
        cls = load_object(mw_path)
        _middlewares.append(cls())
    return _middlewares


class MiddlewareLoader:
    def __init__(self, settings: Dict = None):
        if settings is None:
            settings = context.settings.get()
        logger.info(settings.get(self.name))
        self._middlewares: List = loads(settings.get(self.name))
        logger.info(self._middlewares)
