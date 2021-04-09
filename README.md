# fspider

#### 介绍

fspider是一款基于python原生协程asyncio的异步网络爬虫框架。 框架灵感来自scrapy,并尽可能实现相关功能

#### 要求

python>=3.7
#### 安装
目前不支持pip安装,下载源码 然后执行```python setup.py install```

#### 教程
#### 创建项目
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