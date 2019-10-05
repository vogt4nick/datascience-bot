#!/usr/bin/python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = {}
with open("./datascience_bot/__init__.py", "r") as ifile:
    exec(ifile.read(), version)

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="datascience_bot",
    version=version["__version__"],
    description="datascience_bot",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vogt4nick/datascience_bot",
    author="vogt4nick",
    author_email="vogt4nick@gmail.com",
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "refresh-weekly-thread = datascience_bot.cli.refresh_weekly_thread:main",
            "moderate-submissions = datascience_bot.cli.moderate_submissions:main",
        ]
    },
    install_requires=requirements,
    include_package_data=True,  # include MANIFEST.in
    test_suite="tests",
    tests_require="pytest",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable Copy",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
