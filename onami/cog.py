# -*- coding: utf-8 -*-

"""
onami.cog
~~~~~~~~~~~~

The onami debugging and diagnostics cog implementation.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""


import nextcord
from nextcord.ext import commands

from .meta import __version__


build = "21"

try:
    print(f"Loading Onami v{__version__}")

except:
    print("Failed to load Onami")

finally:
    print(f"Onami has loaded into build {build}")

from onami.features.filesystem import FilesystemFeature
from onami.features.guild import GuildFeature
from onami.features.invocation import InvocationFeature
from onami.features.management import ManagementFeature
from onami.features.python import PythonFeature
from onami.features.root_command import RootCommand
from onami.features.shell import ShellFeature
from onami.features.voice import VoiceFeature

__all__ = (
    "Onami",
    "STANDARD_FEATURES",
    "OPTIONAL_FEATURES",
    "setup",
)

STANDARD_FEATURES = (
    VoiceFeature,
    GuildFeature,
    FilesystemFeature,
    InvocationFeature,
    ShellFeature,
    PythonFeature,
    ManagementFeature,
    RootCommand,
)

OPTIONAL_FEATURES = []

try:
    from onami.features.youtube import YouTubeFeature
except ImportError:
    pass
else:
    OPTIONAL_FEATURES.insert(0, YouTubeFeature)


class Onami(
    *OPTIONAL_FEATURES, *STANDARD_FEATURES
):  # pylint: disable=too-few-public-methods
    """
    The frontend subclass that mixes in to form the final onami cog.
    """


def setup(bot: commands.Bot):
    """
    The setup function defining the onami.cog and onami extensions.
    """

    bot.add_cog(Onami(bot=bot))
