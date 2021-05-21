# fspider

#### 介绍

fspider是一款基于python原生协程asyncio的异步网络爬虫框架。 框架灵感来自scrapy,并尽可能实现相关功能

#### 要求

python>=3.7

#### 安装

目前不支持pip安装,下载源码 然后执行```python setup.py install```

#### 教程

##### 创建项目

fspdier startproject 命令有两个参数-项目名称和项目路径
```fspdier startproject testspider .``` 在当前目录创建testspider项目

```
cd testspider
python main.py
```

执行默认的测试用例

#### command

在命令行窗口使用fspider -h 查看支持的命令及参数

- fspdier startproject -h
- fspdier shell -h

#### 上下文变量

```
from fspider import context
context.spider.get()
```

目前支持spider对象的获取，这样就不必将spider一直作为参数来传递。
<span style="color:red">注意:必须在spider初始化之后，即无法在spider init 里面调用</span>

#### signals

- spdier_opened
- spider_closed

使用方法:
spider 默认绑定了这两个signal 你可以覆盖这两个方法

```python
async def spider_opened(self):
    self.logger.info('spider_opened!!!!!!!!!!!')


async def spider_closed(self):
    self.logger.info('spider_closed ')
    pass
```

在其他地方使用(sender参数默认使用```context.spider.get()```)

```python
from fspider import signals


async def spider_opened():
    pass


signals.connect(receiver=spider_opened, signal=signals.spider_opened)
```

#### spider middreware

spider middreware 是用来处理spider结果的组件 一个简单的spider middreware 如下所示：

```python
from fspider.http.response import Response
from fspider.spidermiddlewares import SpiderMiddleware
from fspider.utils.type import SpiderRequest


class TestSpiderMiddleware(SpiderMiddleware):
    async def process_start_requests(self, result: SpiderRequest) -> SpiderRequest:
        async for r in result:
            print('process_start_requests', r)
            yield r

    async def process_spider_output(self, response: Response, result: SpiderRequest) -> SpiderRequest:
        async for i in result:
            print('process_spider_output', i)
            yield i
```

之后你需要在setting中配置启用：

```python
SPIDER_MIDDLEWARES = {
    'test.middlewares.TestSpiderMiddleware': 543,
}
```

#### downloader middreware

downloader middreware 是用来处理request请求，最终得到response的一系列组件， 一个简单的downloader middreware 如下所示

```python
from typing import Union
from fspider.downloadermiddlewares import DownloaderMiddleware
from fspider.http.request import Request
from fspider.http.response import Response


class TestDownloaderMiddleware(DownloaderMiddleware):
    async def process_request(self, request: Request) -> Union[Request, Response, None]:
        print('process_request', request)
        return None

    async def process_response(self, request: Request, response: Response) -> Union[Request, Response]:
        print('process_response', response)
        return response

```

之后你需要在setting中配置启用：

```python
DOWNLOADER_MIDDLEWARES = {
    'test.middlewares.TestDownloaderMiddleware': 543,
}
```

> DOWNLOADER_MIDDLEWARES 会先顺序执行各个middlewares的process_request方法，之后倒叙执行process_response

#### 内置 downloader middreware

##### RobotsTxtMiddleware

##### DownloadTimeoutMiddleware

##### DefaultHeadersMiddleware

```python
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,en;q=0.7,la;q=0.6,ja;q=0.5',
    'accept-encoding': 'gzip, deflate, br',
}
```

##### HttpCompressionMiddleware

aiohttp 会根据response 自动解压数据，所以不需要实现该中间件 （默认DEFAULT_REQUEST_HEADERS 'accept-encoding': 'gzip, deflate,
br'，接受压缩数据，不需要的话可以删除accept-encoding）

##### UserAgentMiddleware

##### CookiesMiddleware

##### DefaultDownloaderMiddleware
