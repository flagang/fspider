import os
from configparser import ConfigParser
from importlib import import_module


def get_settings():
    setting = {}
    md = get_settings_moudle()
    module = import_module(md)
    for key in dir(module):
        setting[key] = getattr(module, key)
    return setting


def get_settings_moudle():
    current_dir = os.getcwd()
    cfg = ConfigParser()
    path = os.path.join(current_dir, 'fspider.cfg')
    if os.path.exists():
        cfg.read(path)
        return cfg.get('settings', 'default')
    return f'{os.path.basename()}.settings'
