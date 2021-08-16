import logging
import os
from configparser import ConfigParser
from importlib import import_module
from typing import Dict

from fspider.utils import default_settings


def get_md_map(module):
    settings = {}
    for key in dir(module):
        if key.isupper():
            settings[key] = getattr(module, key)
    return settings


def get_default_settings() -> Dict:
    return get_md_map(default_settings)


def get_settings() -> Dict:
    try:
        md = get_settings_moudle()
        module = import_module(md)
        settings = get_md_map(module)
    except ModuleNotFoundError:
        logging.exception(f'settings {md}  ModuleNotFoundError use default_settings ')
        settings = {}
    df_settings = get_default_settings()
    for k, v in settings.items():
        if isinstance(v, Dict) and k in df_settings:
            df_settings[k].update(v)
        else:
            df_settings[k] = v
    return df_settings


def get_settings_moudle():
    current_dir = os.getcwd()
    cfg = ConfigParser()
    path = os.path.join(current_dir, 'fspider.cfg.tmpl')
    if os.path.exists(path):
        cfg.read(path)
        return cfg.get('settings', 'default')
    return f'{os.path.basename(current_dir)}.settings'
