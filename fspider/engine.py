import random
from asyncio import iscoroutine, iscoroutinefunction

from typing import Type, List, Union, Callable, Coroutine, Any
from fspider.http.downloader import down, close
from fspider.http.request import Request
from fspider.spider import Spider
import asyncio
import logging
import signal

HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)


class Worker:
    def __init__(self, spider: Spider, num):
        self.spider = spider
        self._scheduler = spider._scheduler
        self._num = num
        self.idle = set()  # 空闲worker 编号
        self._close_signal = False  # 是否接收到singal 信号

    async def run(self):
        if len(self._scheduler) == 0:
            async for resquest in self.spider.start_requests():
                self._scheduler.push_request(resquest)
        tasks = [self.start_worker(i) for i in range(self._num)]
        await asyncio.gather(*tasks, return_exceptions=True)

    def close(self):
        """
        调用此方法说明程序接收到关闭信号
        :return:
        """
        self._close_signal = True

    async def start_worker(self, work_no: int):
        logging.info(f'worker {work_no} start!')
        while not self._close_signal:
            request = self._scheduler.pop_request()
            if request:
                logging.info(f'worker_{work_no}: begin process {request}')
                if work_no in self.idle:
                    self.idle.remove(work_no)
                await self.work(request)
                logging.info(f'worker_{work_no}: end process {request}')
            else:
                self.idle.add(work_no)
                await asyncio.sleep(1)
                if len(self.idle) == self._num:  # 所有worker都空闲表示任务完成
                    logging.info(f'all task idle worker {work_no} end')
                    break

    async def work(self, request: Request):
        try:
            callback = request.callback
            response = await down(request)
            await asyncio.sleep(random.randint(10, 15) / 10)
            async for result in callback(response):
                if isinstance(result, Request):
                    self._scheduler.push_request(result)
                else:
                    if result:
                        logging.info(f'success save {result}')
        except Exception:
            logging.exception(f'error while process {request}')
            # if self.spider.settings.get('',False):
            self._scheduler.remove_dupefilter(request)


class Crawler:
    _spiders: List[Type[Spider]] = []

    def __init__(self):
        self.loop = None
        self._running_worker: List[Worker] = []  # 记录正在运行的爬虫name
        self.should_exit = False  # True 表示第一次接收signal
        self.force_exit = False  # True 表示第二次接收signal 強制关闭
        self.jobs = []

    def add_spider(self, sipder_cls: Type[Spider]):
        self._spiders.append(sipder_cls)

    async def _crawl(self, spider_cls: Type[Spider]):
        worker = None
        try:
            spider = await spider_cls.create_spider()
            await spider.spider_opened()
            settings = spider.settings
            workers = settings.get('workers')
            worker = Worker(spider, workers)
            self._running_worker.append(worker)
            await worker.run()
            await spider.spider_closed()
        except Exception:
            logging.exception(f'Spider  {spider_cls.name} error')
        finally:
            if worker:
                self._running_worker.remove(worker)

    async def crawl(self, spider_cls: Type[Spider]):
        """
        添加协程任务 不等待 可以使用apscheduler 定时任务
        :param sipder_cls:
        :return:
        """
        asyncio.create_task(self._crawl(spider_cls))

    def all_spider_finished(self):
        if not self.stop:  # run forever
            return False
        if len(self._running_worker) > 0:
            return False
        return True

    def handle_exit(self, sig, frame):
        if self.should_exit:  # 第二次接收 强制关闭
            self.force_exit = True
        else:  # 第一次接收signal 向各个爬虫任务发送关闭信号 等待关闭
            self.should_exit = True

    def install_signal_handlers(self):
        try:
            for sig in HANDLED_SIGNALS:
                self.loop.add_signal_handler(sig, self.handle_exit, sig, None)
        except NotImplementedError:
            # Windows
            for sig in HANDLED_SIGNALS:
                signal.signal(sig, self.handle_exit)

    def stop_workers(self):
        for worker in self._running_worker:
            worker.close()

    async def start(self):
        self.loop = asyncio.get_event_loop()
        self.install_signal_handlers()
        self.start_job()
        for spider_cls in self._spiders:
            await self.crawl(spider_cls)
        await asyncio.sleep(0)  # 交出控制权 执行self._spiders 爬虫任务

        # 如果是接收了signal关闭信号 调用stop_workers() 等待所有爬虫任务结束 或者再次接收到signal
        # 如果是all_spider_finished() 为True 表明爬虫任务结束 终止程序
        while not self.all_spider_finished() and not self.should_exit:
            await asyncio.sleep(0.5)
        if self.should_exit:
            self.stop_workers()
        while not self.all_spider_finished() and not self.force_exit:
            await asyncio.sleep(0.5)

    def start_job(self):
        for job in self.jobs:
            if iscoroutinefunction(job):
                asyncio.create_task(job(self))
            else:
                job(self)

    def add_job(self, job: Callable[["Crawler"], Any]):
        self.jobs.append(job)

    def run(self, stop=True):
        self.stop = stop
        asyncio.run(self.start())


def start_spider(cls):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    crawler = Crawler()
    crawler.add_spider(cls)
    crawler.run()
