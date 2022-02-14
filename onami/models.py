# -*- coding: utf-8 -*-

"""
onami.models
~~~~~~~~~~~~~~

Functions for modifying or interfacing with nextcord models.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import copy

import nextcord as nextcord
from nextcord.ext import commands


async def copy_context_with(
    ctx: commands.Context, *, author=None, channel=None, **kwargs
):
    """
    Makes a new :class:`Context` with changed message properties.
    """

    # copy the message and update the attributes
    alt_message: nextcord.Message = copy.copy(ctx.message)
    alt_message._update(kwargs)  # pylint: disable=protected-access

    if author is not None:
        alt_message.author = author
    if channel is not None:
        alt_message.channel = channel

    # obtain and return a context of the same type
    return await ctx.bot.get_context(alt_message, cls=type(ctx))
