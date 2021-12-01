import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

import datetime

from defaults import defaults

class Info(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(
    name="avatar",
    description="View someone's avatar",
    options=[
      create_option(
        name="user",
        description="The user to get the avatar from",
        option_type=6,
        required=False
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def _avatar(self, ctx: SlashContext, user: discord.Member=None):
    await ctx.defer()

    user = user if user else ctx.author

    avEmbed = discord.Embed(
      title=f"{user.display_name}'s avatar",
      color=defaults.color
    )

    avEmbed.set_image(url=user.avatar_url)

    avEmbed.set_footer(**defaults.footer(ctx.author))
    avEmbed.timestamp = datetime.datetime.utcnow()

    await ctx.send(embed=avEmbed)

def setup(bot):
  bot.add_cog(Info(bot))