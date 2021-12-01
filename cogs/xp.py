import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

class Xp(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_subcommand(
    base="xp",
    name="level",
    description="Check someone's xp level",
    base_description="XP",
    options=[
      create_option(
        name="user",
        description="The user to get the xp for (Leave blank to view your own)",
        option_type=6,
        required=False
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def xp_level(self, ctx: SlashContext, user: discord.Member=None):
    ctx.defer()


def setup(bot):
  bot.add_cog(Xp(bot))