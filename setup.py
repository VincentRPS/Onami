#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2021 Devon (Gorialis) R
Copyright (c) 2021 VincentRPS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pathlib

from setuptools import setup

ROOT = pathlib.Path(__file__).parent

VERSION = f'2.6.3'

EXTRA_REQUIRES = {}

for feature in (ROOT / "requirements").glob("*.txt"):
    with open(feature, "r", encoding="utf-8") as f:
        EXTRA_REQUIRES[feature.with_suffix("").name] = f.read().splitlines()


REQUIREMENTS = EXTRA_REQUIRES.pop("_")


with open(ROOT / "README.md", "r", encoding="utf-8") as f:
    README = f.read()


setup(
    name="onami",
    author="VincentRPS",
    url="https://github.com/VincentRPS/Onami",
    license="MIT",
    description="A pythonic nextcord extension including useful tools for bot development and debugging.",
    long_description=README,
    long_description_content_type="text/markdown",
    project_urls={
        "Documentation": "https://onami.readthedocs.io/en/latest/",
        "Code": "https://github.com/VincentRPS/Onami",
        "Issue tracker": "https://github.com/VincentRPS/Onami/issues",
        "Pull tracker": "https://github.com/VincentRPS/Onami/pulls",
        "Projects": "https://github.com/VincentRPS/Onami/projects",
    },
    version=VERSION,
    packages=["onami", "onami.features", "onami.repl", "onami.shim"],
    include_package_data=True,
    install_requires=REQUIREMENTS,
    python_requires=">=3.8.0",
    extras_require=EXTRA_REQUIRES,
    keywords="onami nextcord nextcord cog repl extension onami",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Internet",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
    ],
)
