# -*- coding: utf-8 -*-

"""
jishaku subclassing test 1
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a valid extension file for nextcord intended to
discover weird behaviors related to subclassing.

This variant overrides behavior using a Feature.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import jishaku
from nextcord.ext import commands


class ThirdPartyFeature(jishaku.Feature):
    """
    overriding feature for test
    """

    @jishaku.Feature.Command(
        name="jishaku", aliases=["jsk"], invoke_without_command=True, ignore_extra=False
    )
    async def jsk(self, ctx: commands.Context):
        """
        override test
        """
        return await ctx.send(
            "The behavior of this command has been overridden with a third party feature."
        )


class Magnet1(
    ThirdPartyFeature, *jishaku.OPTIONAL_FEATURES, *jishaku.STANDARD_FEATURES
):  # pylint: disable=too-few-public-methods
    """
    The extended Jishaku cog
    """


def setup(bot: commands.Bot):
    """
    The setup function for the extended cog
    """

    bot.add_cog(Magnet1(bot=bot))
