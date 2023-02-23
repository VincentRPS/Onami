# -*- coding: utf-8 -*-

"""
onami.features.root_command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The onami root command.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import math
import sys
import typing

import nextcord
from nextcord.ext import commands

from onami.features.baseclass import Feature
from onami.flags import Flags
from onami.modules import package_version
from onami.paginators import PaginatorInterface

try:
    import psutil
except ImportError:
    psutil = None

try:
    from importlib.metadata import packages_distributions
except ImportError:
    from importlib_metadata import packages_distributions


def natural_size(size_in_bytes: int):
    """
    Converts a number of bytes to an appropriately-scaled unit
    E.g.:
        1024 -> 1.00 KiB
        12345678 -> 11.77 MiB
    """
    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")

    power = int(math.log(size_in_bytes, 1024))

    return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"


class RootCommand(Feature):
    """
    Feature containing the root oni command
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oni.hidden = Flags.HIDE

    @Feature.Command(
        name="onami", aliases=["oni"], invoke_without_command=True, ignore_extra=False
    )
    async def oni(self, ctx: commands.Context):  # pylint: disable=too-many-branches
        """
        The onami debug and diagnostic commands.

        This command on its own gives a status brief.
        All other functionality is within its subcommands.
        """

        package_name = packages_distributions()["nextcord"][0]

        summary = [
            f"onami v{package_version('onami')}, {package_name} `{package_version(package_name)}`, "
            f"`Python {sys.version}` on `{sys.platform}`".replace("\n", ""),
            f"Module was loaded <t:{self.load_time.timestamp():.0f}:R>, "
            f"cog was loaded <t:{self.start_time.timestamp():.0f}:R>.",
            "",
        ]

        # detect if [procinfo] feature is installed
        if psutil:
            try:
                proc = psutil.Process()

                with proc.oneshot():
                    try:
                        mem = proc.memory_full_info()
                        summary.append(
                            f"Using {natural_size(mem.rss)} physical memory and "
                            f"{natural_size(mem.vms)} virtual memory, "
                            f"{natural_size(mem.uss)} of which unique to this process."
                        )
                    except psutil.AccessDenied:
                        pass

                    try:
                        name = proc.name()
                        pid = proc.pid
                        thread_count = proc.num_threads()

                        summary.append(
                            f"Running on PID {pid} (`{name}`) with {thread_count} thread(s)."
                        )
                    except psutil.AccessDenied:
                        pass

                    summary.append("")  # blank line
            except psutil.AccessDenied:
                summary.append(
                    "psutil is installed, but this process does not have high enough access rights "
                    "to query process information."
                )
                summary.append("")  # blank line

        cache_summary = (
            f"{len(self.bot.guilds)} guild(s) and {len(self.bot.users)} user(s)"
        )

        # Show shard settings to summary
        if isinstance(self.bot, nextcord.AutoShardedClient):
            if len(self.bot.shards) > 20:
                summary.append(
                    f"This bot is automatically sharded ({len(self.bot.shards)} shards of {self.bot.shard_count})"
                    f" and can see {cache_summary}."
                )
            else:
                shard_ids = ", ".join(str(i) for i in self.bot.shards.keys())
                summary.append(
                    f"This bot is automatically sharded (Shards {shard_ids} of {self.bot.shard_count})"
                    f" and can see {cache_summary}."
                )
        elif self.bot.shard_count:
            summary.append(
                f"This bot is manually sharded (Shard {self.bot.shard_id} of {self.bot.shard_count})"
                f" and can see {cache_summary}."
            )
        else:
            summary.append(f"This bot is not sharded and can see {cache_summary}.")

        # pylint: disable=protected-access
        if self.bot._connection.max_messages:
            message_cache = (
                f"Message cache capped at {self.bot._connection.max_messages}"
            )
        else:
            message_cache = "Message cache is disabled"

        if nextcord.version_info >= (1, 5, 0):
            presence_intent = f"presence intent is {'enabled' if self.bot.intents.presences else 'disabled'}"
            members_intent = f"members intent is {'enabled' if self.bot.intents.members else 'disabled'}"
            message_content_intent = f"message content intent is {'enabled' if self.bot.intents.message_content else 'disabled'}"

            summary.append(f"{message_cache}, {presence_intent}, {members_intent} and {message_content_intent}.")
        else:
            guild_subscriptions = f"guild subscriptions are {'enabled' if self.bot._connection.guild_subscriptions else 'disabled'}"

            summary.append(f"{message_cache} and {guild_subscriptions}.")

        # pylint: enable=protected-access

        # Show websocket latency in milliseconds
        summary.append(
            f"Average websocket latency: {round(self.bot.latency * 1000, 2)}ms"
        )

        await ctx.send("\n".join(summary))

    # pylint: disable=no-member
    @Feature.Command(parent="oni", name="hide")
    async def oni_hide(self, ctx: commands.Context):
        """
        Hides onami from the help command.
        """

        if self.oni.hidden:
            return await ctx.send("onami is already hidden.")

        self.oni.hidden = True
        await ctx.send("onami is now hidden.")

    @Feature.Command(parent="oni", name="show")
    async def oni_show(self, ctx: commands.Context):
        """
        Shows onami in the help command.
        """

        if not self.oni.hidden:
            return await ctx.send("onami is already visible.")

        self.oni.hidden = False
        await ctx.send("onami is now visible.")

    # pylint: enable=no-member

    @Feature.Command(parent="oni", name="tasks")
    async def oni_tasks(self, ctx: commands.Context):
        """
        Shows the currently running onami tasks.
        """

        if not self.tasks:
            return await ctx.send("No currently running tasks.")

        paginator = commands.Paginator(max_size=1985)

        for task in self.tasks:
            paginator.add_line(
                f"{task.index}: `{task.ctx.command.qualified_name}`, invoked at "
                f"{task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )

        interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
        return await interface.send_to(ctx)

    @Feature.Command(parent="oni", name="cancel")
    async def oni_cancel(self, ctx: commands.Context, *, index: typing.Union[int, str]):
        """
        Cancels a task with the given index.

        If the index passed is -1, will cancel the last task instead.
        """

        if not self.tasks:
            return await ctx.send("No tasks to cancel.")

        if index == "~":
            task_count = len(self.tasks)

            for task in self.tasks:
                task.task.cancel()

            self.tasks.clear()

            return await ctx.send(f"Cancelled {task_count} tasks.")

        if isinstance(index, str):
            raise commands.BadArgument('Literal for "index" not recognized.')

        if index == -1:
            task = self.tasks.pop()
        else:
            task = nextcord.utils.get(self.tasks, index=index)
            if task:
                self.tasks.remove(task)
            else:
                return await ctx.send("Unknown task.")

        task.task.cancel()
        return await ctx.send(
            f"Cancelled task {task.index}: `{task.ctx.command.qualified_name}`,"
            f" invoked at {task.ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )
