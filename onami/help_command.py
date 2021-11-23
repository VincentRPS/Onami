# -*- coding: utf-8 -*-

"""
onami.help_command
~~~~~~~~~~~~~~~~~~~~

HelpCommand subclasses with onami features

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

try:
    import nextcord as discord
    from nextcord.ext import commands
    try:
        import disnake as discord
        from disnake.ext import commands

    except(ModuleNotFoundError):
        import discord
        from discord.ext import commands
except:
    pass

from onami.paginators import PaginatorEmbedInterface, PaginatorInterface


class DefaultPaginatorHelp(commands.DefaultHelpCommand):
    """
    A subclass of :class:`commands.DefaultHelpCommand` that uses a PaginatorInterface for pages.
    """

    def __init__(self, **options):
        paginator = options.pop('paginator', commands.Paginator(max_size=1985))

        super().__init__(paginator=paginator, **options)

    async def send_pages(self):
        destination = self.get_destination()

        interface = PaginatorInterface(self.context.bot, self.paginator, owner=self.context.author)
        await interface.send_to(destination)


class DefaultEmbedPaginatorHelp(commands.DefaultHelpCommand):
    """
    A subclass of :class:`commands.DefaultHelpCommand` that uses a PaginatorEmbedInterface for pages.
    """

    async def send_pages(self):
        destination = self.get_destination()

        interface = PaginatorEmbedInterface(self.context.bot, self.paginator, owner=self.context.author)
        await interface.send_to(destination)


class MinimalPaginatorHelp(commands.MinimalHelpCommand):
    """
    A subclass of :class:`commands.MinimalHelpCommand` that uses a PaginatorInterface for pages.
    """

    def __init__(self, **options):
        paginator = options.pop('paginator', commands.Paginator(prefix=None, suffix=None, max_size=1985))

        super().__init__(paginator=paginator, **options)

    async def send_pages(self):
        destination = self.get_destination()

        interface = PaginatorInterface(self.context.bot, self.paginator, owner=self.context.author)
        await interface.send_to(destination)


class MinimalEmbedPaginatorHelp(commands.MinimalHelpCommand):
    """
    A subclass of :class:`commands.MinimalHelpCommand` that uses a PaginatorEmbedInterface for pages.
    """

    async def send_pages(self):
        destination = self.get_destination()

        interface = PaginatorEmbedInterface(self.context.bot, self.paginator, owner=self.context.author)
        await interface.send_to(destination)
