import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

from replit import db

class Database(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(
    name="keys",
    description="List all keys",
    guild_ids=defaults.guildIDs
  )
  @commands.is_owner()
  async def _keys(self, ctx: SlashContext):
    await ctx.defer()

    keyList = [f"**{i + 1}**. {key}" for i, key in enumerate(db.keys())]

    keyN = len(keyList)

    keyList = "\n".join(keyList)

    keysEmbed = discord.Embed(
      title=f"{keyN} {'keys' if keyN != 1 else 'key'} found",
      description=keyList,
      color=defaults.color
    )

    await ctx.send(embed=keysEmbed)

  @cog_ext.cog_subcommand(
    base="key",
    name="view",
    description="View the value of a key",
    options = [
      create_option(
        name="key",
        description="The key to view",
        option_type=3,
        required=True
      )
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.is_owner()
  async def key_view(self, ctx: SlashContext, key):
    await ctx.defer()

    keyEmbed = discord.Embed(
      title=key,
      description=dict(db[key]),
      color=defaults.color
    )

    await ctx.send(embed=keyEmbed)

def setup(bot):
  bot.add_cog(Database(bot))