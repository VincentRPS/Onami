# -*- coding: utf-8 -*-

"""
onami.features.management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The onami extension and bot control commands.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import itertools
import math
import time
import traceback
from urllib.parse import urlencode

import nextcord
from nextcord.ext import commands

from onami.features.baseclass import Feature
from onami.flags import Flags
from onami.modules import ExtensionConverter
from onami.paginators import WrappedPaginator


class ManagementFeature(Feature):
    """
    Feature containing the extension and bot control commands
    """

    @Feature.Command(parent="oni", name="load", aliases=["reload"])
    async def oni_load(self, ctx: commands.Context, *extensions: ExtensionConverter):
        """
        Loads or reloads the given extension names.

        Reports any extensions that failed to load.
        """

        paginator = WrappedPaginator(prefix="", suffix="")

        # 'oni reload' on its own just reloads onami
        if ctx.invoked_with == "reload" and not extensions:
            extensions = [["onami"]]

        for extension in itertools.chain(*extensions):
            method, icon = (
                (
                    self.bot.reload_extension,
                    "\N{CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS}",
                )
                if extension in self.bot.extensions
                else (self.bot.load_extension, "\N{INBOX TRAY}")
            )

            try:
                method(extension)
            except Exception as exc:  # pylint: disable=broad-except
                traceback_data = "".join(
                    traceback.format_exception(type(exc), exc, exc.__traceback__, 1)
                )

                paginator.add_line(
                    f"{icon}\N{WARNING SIGN} `{extension}`\n```py\n{traceback_data}\n```",
                    empty=True,
                )
            else:
                paginator.add_line(f"{icon} `{extension}`", empty=True)

        for page in paginator.pages:
            await ctx.send(page)

    @Feature.Command(parent="oni", name="unload")
    async def oni_unload(self, ctx: commands.Context, *extensions: ExtensionConverter):
        """
        Unloads the given extension names.

        Reports any extensions that failed to unload.
        """

        paginator = WrappedPaginator(prefix="", suffix="")
        icon = "\N{OUTBOX TRAY}"

        for extension in itertools.chain(*extensions):
            try:
                self.bot.unload_extension(extension)
            except Exception as exc:  # pylint: disable=broad-except
                traceback_data = "".join(
                    traceback.format_exception(type(exc), exc, exc.__traceback__, 1)
                )

                paginator.add_line(
                    f"{icon}\N{WARNING SIGN} `{extension}`\n```py\n{traceback_data}\n```",
                    empty=True,
                )
            else:
                paginator.add_line(f"{icon} `{extension}`", empty=True)

        for page in paginator.pages:
            await ctx.send(page)

    @Feature.Command(parent="oni", name="shutdown", aliases=["logout"])
    async def oni_shutdown(self, ctx: commands.Context):
        """
        Logs this bot out.
        """

        ellipse_character = (
            "\N{BRAILLE PATTERN DOTS-356}"
            if Flags.USE_BRAILLE_J
            else "\N{HORIZONTAL ELLIPSIS}"
        )

        await ctx.send(f"Logging out now{ellipse_character}")
        await ctx.bot.close()

    @Feature.Command(parent="oni", name="invite")
    async def oni_invite(self, ctx: commands.Context, *perms: str):
        """
        Retrieve the invite URL for this bot.

        If the names of permissions are provided, they are requested as part of the invite.
        """

        scopes = ("bot", "applications.commands")
        permissions = nextcord.Permissions()

        for perm in perms:
            if perm not in dict(permissions):
                raise commands.BadArgument(f"Invalid permission: {perm}")

            setattr(permissions, perm, True)

        application_info = await self.bot.application_info()

        query = {
            "client_id": application_info.id,
            "scope": "+".join(scopes),
            "permissions": permissions.value,
        }

        return await ctx.send(
            f"Link to invite this bot:\n<https://nextcord.com/oauth2/authorize?{urlencode(query, safe='+')}>"
        )

    @Feature.Command(parent="oni", name="rtt", aliases=["ping"])
    async def oni_rtt(self, ctx: commands.Context):
        """
        Calculates Round-Trip Time to the API.
        """

        message = None

        # We'll show each of these readings as well as an average and standard deviation.
        api_readings = []
        # We'll also record websocket readings, but we'll only provide the average.
        websocket_readings = []

        # We do 6 iterations here.
        # This gives us 5 visible readings, because a request can't include the stats for itself.
        for _ in range(6):
            # First generate the text
            text = "Calculating round-trip time...\n\n"
            text += "\n".join(
                f"Reading {index + 1}: {reading * 1000:.2f}ms"
                for index, reading in enumerate(api_readings)
            )

            if api_readings:
                average = sum(api_readings) / len(api_readings)

                if len(api_readings) > 1:
                    stddev = math.sqrt(
                        sum(math.pow(reading - average, 2) for reading in api_readings)
                        / (len(api_readings) - 1)
                    )
                else:
                    stddev = 0.0

                text += f"\n\nAverage: {average * 1000:.2f} \N{PLUS-MINUS SIGN} {stddev * 1000:.2f}ms"
            else:
                text += "\n\nNo readings yet."

            if websocket_readings:
                average = sum(websocket_readings) / len(websocket_readings)

                text += f"\nWebsocket latency: {average * 1000:.2f}ms"
            else:
                text += f"\nWebsocket latency: {self.bot.latency * 1000:.2f}ms"

            # Now do the actual request and reading
            if message:
                before = time.perf_counter()
                await message.edit(content=text)
                after = time.perf_counter()

                api_readings.append(after - before)
            else:
                before = time.perf_counter()
                message = await ctx.send(content=text)
                after = time.perf_counter()

                api_readings.append(after - before)

            # Ignore websocket latencies that are 0 or negative because they usually mean we've got bad heartbeats
            if self.bot.latency > 0.0:
                websocket_readings.append(self.bot.latency)
