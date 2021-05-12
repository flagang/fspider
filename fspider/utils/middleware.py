import logging
import pprint
from typing import Dict, List

from fspider import context
from fspider.exceptions import NotConfigured
from fspider.utils.misc import load_object
from fspider.utils.type import MiddlewareSetting

logger = logging.getLogger(__name__)


def loads(mw_settings: MiddlewareSetting) -> List:
    _middlewares = []
    mwlist = {k: v for k, v in mw_settings.items() if v is not None}
    mw_paths: List[str] = sorted(mwlist, key=mwlist.get)
    for mw_path in mw_paths:
        try:
            cls = load_object(mw_path)
            _middlewares.append(cls())
        except NotConfigured:
            pass
    return _middlewares


class Middleware:
    def __init__(self, settings: Dict = None):
        if settings is None:
            settings = context.settings.get()
        self.settings = settings


class MiddlewareLoader(Middleware):
    def __init__(self, settings: Dict = None):
        super().__init__(settings)
        self._middlewares: List = loads(self.settings.get(self.name))
        logger.info(pprint.pformat(self._middlewares))
