import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

import requests
import json

class Music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.apiKey = "674d04249ce2ac514b41cb0fd5496d05"

  @cog_ext.cog_slash(
    name="lyrics",
    description="Get the lyrics of a song",
    options=[
      create_option(
        name="song",
        description="The song to get the lyrics for",
        option_type=3,
        required=True
      ),
      create_option(
        name="artist",
        description="The artist of the song",
        option_type=3,
        required=False
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def _lyrics(self, ctx: SlashContext, song: str, artist: str=None):
    await ctx.defer()

    artist = artist if artist else ""

    track = json.loads(requests.get(f"http://api.musixmatch.com/ws/1.1/track.search?q_track={song}&q_artist={artist}&apikey={self.apiKey}").text)
    trackID = track["message"]["body"]["track_list"][0]["track"]["track_id"]

    lyrics = json.loads(requests.get(f"http://api.musixmatch.com/ws/1.1/track.lyrics.get?track_id={trackID}&apikey={self.apiKey}").text)

    await ctx.send("This shit doesn't work yet")

def setup(bot):
  bot.add_cog(Music(bot))