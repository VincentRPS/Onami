# -*- coding: utf-8 -*-

"""
onami.features.shell
~~~~~~~~~~~~~~~~~~~~~~~~

The onami shell commands.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

from nextcord.ext import commands

from onami.codeblocks import Codeblock, codeblock_converter
from onami.cog import build
from onami.exception_handling import ReplResponseReactor
from onami.features.baseclass import Feature
from onami.meta import __version__
from onami.paginators import PaginatorInterface, WrappedPaginator
from onami.shell import ShellReader


class ShellFeature(Feature):
    """
    Feature containing the shell-related commands
    """

    @Feature.Command(
        parent="oni",
        name="shell",
        aliases=["bash", "sh", "powershell", "ps1", "ps", "cmd"],
    )
    async def oni_shell(self, ctx: commands.Context, *, argument: codeblock_converter):
        """
        Executes statements in the system shell.

        This uses the system shell as defined in $SHELL, or `/bin/bash` otherwise.
        Execution can be cancelled by closing the paginator.
        """

        async with ReplResponseReactor(ctx.message):
            with self.submit(ctx):
                with ShellReader(argument.content) as reader:
                    prefix = "```" + reader.highlight

                    paginator = WrappedPaginator(prefix=prefix, max_size=1975)
                    paginator.add_line(f"{reader.ps1} {argument.content}\n")

                    interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
                    self.bot.loop.create_task(interface.send_to(ctx))

                    async for line in reader:
                        if interface.closed:
                            return
                        await interface.add_line(line)

                await interface.add_line(f"\n[status] Return code {reader.close_code}")

    @Feature.Command(parent="oni", name="git")
    async def oni_git(self, ctx: commands.Context, *, argument: codeblock_converter):
        """
        Shortcut for 'oni sh git'. Invokes the system shell.
        """

        return await ctx.invoke(
            self.oni_shell,
            argument=Codeblock(argument.language, "git " + argument.content),
        )

    @Feature.Command(parent="oni", name="version")
    async def oni_version(self, ctx: commands.Context):
        """
        Version showing
        """

        await ctx.reply(f"Onami version {__version__} and build {build}")

    @Feature.Command(parent="oni", name="pip")
    async def oni_pip(self, ctx: commands.Context, *, argument: codeblock_converter):
        """
        Shortcut for 'oni sh pip'. Invokes the system shell.
        """

        return await ctx.invoke(
            self.oni_shell,
            argument=Codeblock(argument.language, "pip " + argument.content),
        )
