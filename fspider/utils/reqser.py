"""
Helper functions for serializing (and deserializing) requests.
"""
import inspect

from fspider.http.request import Request
from fspider.spider import Spider
from fspider.utils.misc import load_object


def request_to_dict(request: Request, spider: Spider = None) -> dict:
    """Convert Request object to a dict.

    If a spider is given, it will try to find out the name of the spider method
    used in the callback and store that as the callback.
    """
    cb = request.callback
    if callable(cb):
        _cb = cb.__name__
    d = {
        'url': request.url,
        'callback': _cb,
        'method': request.method,
        'headers': dict(request.headers),
        'data': request.data,
        'json': request.json,
        'timeout': request.timeout,
        'dont_filter': request.dont_filter,
        'meta': request.meta,
        'kwargs': request.kwargs,
    }
    if type(request) is not Request:
        d['_class'] = request.__module__ + '.' + request.__class__.__name__
    return d


def request_from_dict(d: dict, spider: Spider = None) -> Request:
    """Create Request object from a dict.

    If a spider is given, it will try to resolve the callbacks looking at the
    spider for methods with the same name.
    """
    cb = d['callback']
    if cb and spider:
        cb = _get_method(spider, cb)
    request_cls = load_object(d['_class']) if '_class' in d else Request
    return request_cls(
        url=d['url'],
        callback=cb,
        method=d['method'],
        headers=d['headers'],
        data=d['data'],
        json=d['json'],
        timeout=d['timeout'],
        dont_filter=d['dont_filter'],
        meta=d['meta'],
             ** d['kwargs'],
    )


def _find_method(obj, func):
    if obj:
        try:
            func_self = func.__self__
        except AttributeError:  # func has no __self__
            pass
        else:
            if func_self is obj:
                members = inspect.getmembers(obj, predicate=inspect.ismethod)
                for name, obj_func in members:
                    # We need to use __func__ to access the original
                    # function object because instance method objects
                    # are generated each time attribute is retrieved from
                    # instance.
                    #
                    # Reference: The standard type hierarchy
                    # https://docs.python.org/3/reference/datamodel.html
                    if obj_func.__func__ is func.__func__:
                        return name
    raise ValueError("Function %s is not a method of: %s" % (func, obj))


def _get_method(obj, name):
    name = str(name)
    try:
        return getattr(obj, name)
    except AttributeError:
        raise ValueError("Method %r not found in: %s" % (name, obj))
