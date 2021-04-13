from typing import Dict, Union, List
from fspider.utils.misc import load_object
from fspider.utils.type import MiddlewareSetting


def loads(mw_settings: MiddlewareSetting) -> List:
    _middlewares = []
    mwlist = {k: v for k, v in mw_settings.items() if v is not None}
    mw_paths: List[str] = sorted(mwlist, key=mwlist.get)
    for mw_path in mw_paths:
        cls = load_object(mw_path)
        _middlewares.append(cls())
    return _middlewares
