# -*- coding: utf-8 -*-

"""
Onami
~~~~~~

A pythonic nextcord extension including useful tools for bot development and debugging.

:copyright: (c) 2021 Devon (Gorialis) R & 2021 VincentRPS
:license: MIT, see LICENSE for more details.

"""

# pylint: disable=wildcard-import
from onami.cog import *  # noqa: F401
from onami.features.baseclass import Feature  # noqa: F401
from onami.flags import Flags  # noqa: F401
from onami.meta import *  # noqa: F401

__all__ = ("Onami", "Feature", "Flags", "setup")
