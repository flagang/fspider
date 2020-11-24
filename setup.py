import codecs
import os

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf8').read()


setup(
    name="fspider",
    version="1.0.0",
    description="基于asyncio异步爬虫网络框架，仿scrapy",
    long_description=read("README.txt"),
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
        'aiohttp>=3.6.2',
        'fastapi>=0.54.2',
        'redis>=3.5.1'
    ],
    entry_points={
        'console_scripts': ['fspider = fspider.cmdline:execute']
    },
    keywords="async spider",
    author="feng",
    author_email="793168048@qq.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
)
