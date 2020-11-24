from argparse import Namespace
from code import InteractiveConsole

import asyncio

from fspider.commands import CMD
from fspider.http.downloader import get, down
from fspider.http.request import Request


class SpiderCMD(CMD):
    def help(self) -> str:
        return 'crawl [url]'

    def add_arguments(self):
        self.cmd.add_argument('url', help='the url to crawl', type=str)
        self.cmd.add_argument('--timeout', '-t', help='timeout', default=10, type=int)

    def get_banner(self, namespaces):
        l = []
        for k, v in namespaces.items():
            l.append(f'{k}: {v}')
        return '\n'.join(l)

    async def main(self, request: Request):
        response = await down(request)
        namespaces = {'response': response}
        console = InteractiveConsole(namespaces)
        console.interact(banner=self.get_banner(namespaces))

    def run(self, args: Namespace):
        asyncio.run(self.main(Request(args.url, args.timeout)))


