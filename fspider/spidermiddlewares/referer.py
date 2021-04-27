import logging
from urllib.parse import urlparse, urlunparse

from fspider import context
from fspider.http.request import Request
from fspider.http.response import Response
from fspider.spidermiddlewares import SpiderMiddleware
from fspider.utils.type import SpiderResult

logger = logging.getLogger(__name__)


def origin(url):
    strip_url(url, origin_only=True)


def strip_url(url, origin_only=False):
    """
    参考 https://www.w3.org/TR/referrer-policy/#strip-url
    去除敏感信息如username
    :param url:
    :param origin_only:
    :return:
    """
    if not url:
        return None
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    if origin_only and (parsed_url.username or parsed_url.password):
        netloc = netloc.split('@')[-1]
    if parsed_url.port:
        if (parsed_url.scheme, parsed_url.port) in (('http', 80),
                                                    ('https', 443),
                                                    ('ftp', 21)):
            netloc = netloc.replace(f':{parsed_url.port}', '')
    return urlunparse((
        parsed_url.scheme,
        netloc,
        '/' if origin_only else parsed_url.path,
        '' if origin_only else parsed_url.params,
        '' if origin_only else parsed_url.query,
        ''
    ))


def referer_policy(policy: str, response: Response, request: Request):
    policy = policy.lower()
    _origin = origin(response.url)
    if policy == 'no-referrer':  # 不发送Referer字段。
        return None
    elif policy == 'no-referrer-when-downgrade':
        # https://www.w3.org/TR/referrer-policy/#referrer-policy-no-referrer-when-downgrade
        # 例如 HTTPS -> HTTP 或者 FTPS->FTP 不使用referer 。
        if not urlparse(response.url).scheme in ('https', 'ftps') or \
                urlparse(request.url).scheme in ('https', 'ftps'):
            return strip_url(response.url)
        return None
    elif policy == 'same-origin':
        # 链接到同源网址（协议+域名+端口 都相同）时发送，否则不发送。注意，https://test.com链接到http://test.com也属于跨域。
        if _origin == origin(request.url):
            return strip_url(response.url)
    elif policy == 'origin':  # Referer字段一律只发送源信息（协议+域名+端口），不管是否跨域。
        return _origin
    elif policy == 'strict-origin':  # 如果从 HTTPS 网址链接到 HTTP 网址，不发送Referer字段，其他情况只发送源信息。
        if not urlparse(response.url).scheme in ('https', 'ftps') or \
                urlparse(request.url).scheme in ('https', 'ftps'):
            return _origin
    elif policy == 'origin-when-cross-origin':  # 同源时，发送完整的Referer字段，跨域时发送源信息
        if _origin == origin(request.url):
            return strip_url(response.url)
        else:
            return _origin
    elif policy == 'strict-origin-when-cross-origin':
        # 同源时，发送完整的Referer字段；跨域时，如果 HTTPS 网址链接到 HTTP 网址，不发送Referer字段，否则发送源信息
        if _origin == origin(request.url):
            return strip_url(response.url)
        elif not urlparse(response.url).scheme in ('https', 'ftps') or \
                urlparse(request.url).scheme in ('https', 'ftps'):
            return _origin
    elif policy == 'unsafe-url':  # Referer字段包含源信息、路径和查询字符串，不包含锚点、用户名和密码。
        return strip_url(response.url)


class RefererMiddleware(SpiderMiddleware):

    def __init__(self):
        super(RefererMiddleware, self).__init__()

    async def process_spider_output(self, response: Response, result: SpiderResult) -> SpiderResult:
        async for r in result:
            if isinstance(r, Request):
                if not r.headers.get('Referer'):
                    policy = r.meta.get('Referrer Policy') or response.request.headers.get('Referrer Policy') or \
                             'no-referrer-when-downgrade'
                    if policy:
                        referer = referer_policy(policy, response, r)
                        if referer:
                            r.headers['Referer'] = referer
            yield r
