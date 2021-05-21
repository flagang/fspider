import logging
from asyncio import TimeoutError
from aiohttp.client_exceptions import ClientConnectorError, ClientSSLError

from typing import Union

from fspider import context
from fspider.downloadermiddlewares import DownloaderMiddleware
from fspider.exceptions import NotConfigured
from fspider.http.request import Request
from fspider.http.response import Response

logger = logging.getLogger(__name__)


class RetryMiddleware(DownloaderMiddleware):
    EXCEPTIONS_TO_RETRY = (TimeoutError, ClientConnectorError,
                           ClientSSLError, IOError)

    def __init__(self):
        super(RetryMiddleware, self).__init__()
        if not self.settings.get('RETRY_ENABLED'):
            raise NotConfigured
        self.max_retry_times = self.settings.get('RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in self.settings.get('RETRY_HTTP_CODES'))
        self.priority_adjust = self.settings.get('RETRY_PRIORITY_ADJUST')

    async def process_response(self, request: Request, response: Response) -> Union[Request, Response]:
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response.client_response.reason
            return self._retry(request, reason) or response
        return response

    async def process_exception(self, request: Request, exception: Exception) -> Union[Request, Response, None]:
        if (
                isinstance(exception, self.EXCEPTIONS_TO_RETRY)
                and not request.meta.get('dont_retry', False)
        ):
            return self._retry(request, exception)

    def _retry(self, request: Request, reason: Union[Exception, str]):
        retries = request.meta.get('retry_times', 0) + 1

        retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']
        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': context.spider.get()})
            retryreq = request
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            logger.error("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': context.spider.get()})
