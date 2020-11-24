from argparse import _SubParsersAction, Namespace
import os


class CMD:
    def __init__(self, cmdname: str, sub_parser: _SubParsersAction):
        self.name = cmdname
        self.cmd = sub_parser.add_parser(self.name, help=self.help())
        self.add_arguments()

    def add_arguments(self):
        raise NotImplemented

    def help(self) -> str:
        raise NotImplemented

    def run(self, args: Namespace):
        raise NotImplemented
