# -*- coding: utf-8 -*-

"""
onami.repl
~~~~~~~~~~~~

Repl-related operations and tools for onami.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

# pylint: disable=wildcard-import
from onami.repl.compilation import *  # noqa: F401
from onami.repl.disassembly import disassemble  # noqa: F401
from onami.repl.inspections import all_inspections  # noqa: F401
from onami.repl.repl_builtins import get_var_dict_from_ctx  # noqa: F401
from onami.repl.scope import *  # noqa: F401
