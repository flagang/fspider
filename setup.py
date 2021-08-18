import codecs
import os
from os.path import join, dirname

from setuptools import setup, find_packages


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf8').read()


with open(join(dirname(__file__), 'fspider/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name="fspider",
    version=version,
    description="基于asyncio异步爬虫网络框架，仿scrapy",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    classifiers=
    [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    install_requires=
    [
        'uvicorn>=0.11.5',
        'parsel>=1.6.0',
        'aiohttp==3.7.3',
        'fastapi>=0.54.2',
        'redis>=3.5.1'
        'PyDispatcher>=2.0.5',
        'brotlipy>=0.7.0'

    ],
    entry_points={
        'console_scripts': ['fspider = fspider.cmdline:execute']
    },
    keywords="async spider",
    author="feng",
    author_email="709642236@qq.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # True 的话egg方式安装
)
