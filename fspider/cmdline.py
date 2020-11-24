import argparse

import inspect
from fspider.commands import CMD
from fspider.utils.misc import walk_modules

parser = argparse.ArgumentParser(prog='fspider')
subparsers = parser.add_subparsers(dest='command')


def _iter_command_classes(module_name):
    for module in walk_modules(module_name):
        for obj in vars(module).values():
            if inspect.isclass(obj) and \
                    issubclass(obj, CMD) and \
                    obj.__module__ == module.__name__ and \
                    not obj == CMD:
                yield obj


def _get_commands_from_module(module):
    d = {}
    for cmd in _iter_command_classes(module):
        cmdname = cmd.__module__.split('.')[-1]
        d[cmdname] = cmd(cmdname, subparsers)
    return d


def execute():
    d = _get_commands_from_module('fspider.commands')
    args = parser.parse_args()
    command = args.command
    print(args)
    d[command].run(args)
