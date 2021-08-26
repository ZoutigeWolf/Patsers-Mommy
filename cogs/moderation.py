import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

class Moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(
    name="ban",
    description="Ban a user",
    options=[
      create_option(
        name="user",
        description="User that you want to ban",
        option_type=6,
        required=True,
      ),
      create_option(
        name="reason",
        description="Reason for the ban",
        option_type=3,
        required=False,
      )
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.has_permissions(ban_members=True)
  async def _ban(self, ctx: SlashContext, user: discord.Member, reason=None):
    await ctx.defer()

    if ctx.author.top_role > user.top_role:
      await user.ban(reason=f"Banned by {ctx.author} - \"{reason if reason else 'No reason'}\"")

      banEmbed = discord.Embed(
        description=f"{ctx.author.mention} banned {user.mention}\nReason: `{reason if reason else 'No reason'}`",
        color=defaults.color
      )

      await ctx.send(embed=banEmbed)

    else:
      await ctx.send("You can't kick someone with a higher position than you")

  @cog_ext.cog_slash(
    name="kick",
    description="Kick a user",
    options=[
      create_option(
        name="user",
        description="User that you want to kick",
        option_type=6,
        required=True,
      ),
      create_option(
        name="reason",
        description="Reason for the kick",
        option_type=3,
        required=False,
      )
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.has_permissions(kick_members=True)
  async def _kick(self, ctx: SlashContext, user: discord.Member, reason=None):
    await ctx.defer()

    if ctx.author.top_role > user.top_role:
      await user.kick(reason=f"Kicked by {ctx.author} - \"{reason if reason else 'No reason'}\"")

      kickEmbed = discord.Embed(
        description=f"{ctx.author.mention} kicked {user.mention}\nReason: `{reason if reason else 'No reason'}`",
        color=defaults.color
      )

      await ctx.send(embed=kickEmbed)
    
    else:
      await ctx.send("You can't kick someone with a higher position than you")

def setup(bot):
  bot.add_cog(Moderation(bot))