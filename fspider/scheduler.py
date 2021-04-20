import json
import logging

from typing import Optional, List, Set
from fspider.http.request import Request
from fspider.spider import Spider
import redis
import hashlib

from fspider.utils.reqser import request_to_dict, request_from_dict

logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, spider: Spider):
        self.settings = spider.settings
        self.spider = spider

    def __len__(self) -> int:
        return 0

    def push_request(self, request: Request):
        raise NotImplemented

    def pop_request(self) -> Optional[Request]:
        raise NotImplemented

    def remove_dupefilter(self, request: Request):
        pass

    def request_fingerprint(self, request: Request):
        hl = hashlib.md5()
        hl.update(request.url.encode(encoding='utf-8'))
        return hl.hexdigest()


class PyScheduler(Scheduler):
    def __init__(self, spider: Spider):
        super().__init__(spider)
        self._requests: List[Request] = []
        self._dupefilter: Set[str] = set()

    def push_request(self, request: Request):
        _fingerprint = self.request_fingerprint(request)
        if request.dont_filter is False and _fingerprint in self._dupefilter:
            logger.info(f'{request} dupefilter ')
        else:
            self._requests.append(request)
            self._dupefilter.add(_fingerprint)

    def pop_request(self) -> Optional[Request]:
        if len(self._requests) > 0:
            return self._requests.pop(0)
        return None


class RedisScheduler(Scheduler):
    def __init__(self, spider: Spider):
        super().__init__(spider)
        self.dupefilter_key = '{}:dupefilter'.format(spider.name)
        self.request_key = '{}:request'.format(spider.name)
        print(self.settings)
        self.redis_url = self.settings['redis_url']
        self.server = redis.from_url(self.redis_url)

    def __len__(self) -> int:
        # return self.server.zcard(self.request_key)
        return self.server.llen(self.request_key)

    def remove_dupefilter(self, request: Request):
        if request.dont_filter is False:
            logging.info(f'remove dupefilter  of {request}')
            fp = self.request_fingerprint(request)
            self.server.srem(self.dupefilter_key, fp)

    def push_request(self, request: Request):
        fp = self.request_fingerprint(request)
        # This returns the number of values added, zero if already exists.
        if request.dont_filter is False and self.server.sadd(self.dupefilter_key, fp) == 0:
            logging.info(f'{request} dupefilter ')
        else:
            self.server.rpush(self.request_key, self.decode_request(request))
            # self.server.zadd(self.request_key, {self.decode_request(request): 0})

    def decode_request(self, request: Request) -> str:
        return json.dumps(request_to_dict(request, self.spider))

    def encode_request(self, result: str) -> Request:
        d = json.loads(result)
        return request_from_dict(d, self.spider)

    def pop_request(self) -> Optional[Request]:
        result = self.server.lpop(self.request_key)
        if result:
            return self.encode_request(result.decode())
        # pipe = self.server.pipeline()
        # pipe.multi()
        # pipe.zrange(self.request_key, 0, 0).zremrangebyrank(self.request_key, 0, 0)
        # results, count = pipe.execute()
        # if results:
        #     return self.encode_request(results[0].decode())
        return None
