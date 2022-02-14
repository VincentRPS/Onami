# -*- coding: utf-8 -*-

"""
onami.features.youtube
~~~~~~~~~~~~~~~~~~~~~~~~~

The onami youtube-dl command.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

import nextcord
import yt_dlp
from nextcord.ext import commands

from onami.features.baseclass import Feature
from onami.features.voice import VoiceFeature

BASIC_OPTS = {
    "format": "webm[abr>0]/bestaudio/best",
    "prefer_ffmpeg": True,
    "quiet": True,
}


class BasicYouTubeDLSource(nextcord.FFmpegPCMAudio):
    """
    Basic audio source for yt_dlp-compatible URLs.
    """

    def __init__(self, url, download: bool = False):
        ytdl = yt_dlp.YoutubeDL(BASIC_OPTS)
        info = ytdl.extract_info(url, download=download)
        super().__init__(info["url"])


class YouTubeFeature(Feature):
    """
    Feature containing the youtube-dl command
    """

    @Feature.Command(
        parent="oni_voice", name="youtube_dl", aliases=["youtubedl", "ytdl", "yt"]
    )
    async def oni_vc_youtube_dl(self, ctx: commands.Context, *, url: str):
        """
        Plays audio from yt-dlp-compatible sources.
        """

        if await VoiceFeature.connected_check(ctx):
            return

        voice = ctx.guild.voice_client

        if voice.is_playing():
            voice.stop()

        # remove embed maskers if present
        url = url.lstrip("<").rstrip(">")

        voice.play(nextcord.PCMVolumeTransformer(BasicYouTubeDLSource(url)))
        await ctx.send(f"Playing in {voice.channel.name}.")
