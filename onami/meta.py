# -*- coding: utf-8 -*-

"""
onami.meta
~~~~~~~~~~~~

Meta information about onami.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

from collections import namedtuple

import pkg_resources

__all__ = (
    "__author__",
    "__copyright__",
    "__docformat__",
    "__license__",
    "__title__",
    "__version__",
    "version_info",
)

# pylint: disable=invalid-name
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=2, minor=6, micro=3, releaselevel="final", serial=0)

__author__ = "VincentRPS"
__copyright__ = "Copyright 2021 VincentRPS"
__docformat__ = "restructuredtext en"
__license__ = "MIT"
__title__ = "onami"
__version__ = ".".join(
    map(str, (version_info.major, version_info.minor, version_info.micro))
)

# This ensures that when onami is reloaded, pkg_resources requeries it to provide correct version info
pkg_resources.working_set.by_key.pop("onami", None)
