# -*- coding:utf-8 -*-

from setuptools import setup


setup(
    name = "pydaemon",
    version = "0.1",
    author = "HuiQi",
    license = "MIT",
    url = "https://github.com/tqlihuiqi/pydaemon",
    description = "Python daemonizer process",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        "psutil>=5.2.2",
        "setproctitle>=1.1.10",
    ],
    packages = ["daemon"]
)
