import discord
from discord.ext import commands
from discord.utils import get
from functions import defaultColor, embedAuthor
import datetime

class info(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name="info", invoke_without_command=True)
  async def info(self, ctx):
    await ctx.send("s!info <server / user / role> [item]")
  
  @info.command(name="server")
  async def server_subcommand(self, ctx):
    guild = ctx.guild

    infoFields = {
      "id": guild.id,
      "Description": guild.description,
      "Members": guild.member_count,
      "Region": guild.region,
      "AFK Timeout": guild.afk_timeout,
      "AFK Channel": guild.afk_channel,
      "Owner": guild.owner.mention,
      "Boost tier": guild.premium_tier,
      "Boost amount": guild.premium_subscription_count,
      "Booster role": guild.premium_subscriber_role.mention,
      "Channels": len(guild.channels),
      "Text channels": len(guild.text_channels),
      "Voice channels": len(guild.voice_channels),
      "Stage channels": len(guild.stage_channels),
      "Categories": len(guild.categories),
    }

    infoFieldsInline = {
      "id": True,
      "Description": True,
      "Members": True,
      "Region": True,
      "AFK Timeout": True,
      "AFK Channel": True,
      "Owner": True,
      "Boost tier": True,
      "Boost amount": True,
      "Booster role": True,
      "Channels": True,
      "Text channels": True,
      "Voice channels": True,
      "Stage channels": True,
      "Categories": True,
    }

    serverInfoEmbed = discord.Embed(
      title=guild.name,
      description=f"Created at {guild.created_at.ctime()}",
      color=defaultColor
    )

    for name, val in infoFields.items():
      serverInfoEmbed.add_field(
        name=name,
        value=val,
        inline=infoFieldsInline[name]
      )

    serverInfoEmbed.set_author(**embedAuthor)
    serverInfoEmbed.timestamp = datetime.datetime.utcnow()
    serverInfoEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    serverInfoEmbed.set_thumbnail(url=guild.icon_url)

    await ctx.send(embed=serverInfoEmbed)

  @info.command(name="user")
  async def user_subcommand(self, ctx, user: discord.Member=None):
    if user is None:
      user = ctx.author

    

    booster = (True if user in ctx.guild.premium_subscribers else False)
    owner = (True if user == ctx.guild.owner else False)

    infoFields = {
      "Discriminator": user.discriminator,
      "Nickname": user.display_name,
      "Bot": user.bot,
      "Booster": booster,
      "Server Owner": owner,
      "Roles": len(user.roles),
      "Created at": user.created_at.ctime(),
      "Joined at": user.joined_at.ctime(),
      "Booster since": user.premium_since.ctime()
    }

    infoFieldsInline = {
      "Discriminator": True,
      "Nickname": True,
      "Bot": True,
      "Booster": True,
      "Server Owner": True,
      "Roles": True,
      "Created at": False,
      "Joined at": False,
      "Booster since": False
    }

    serverInfoEmbed = discord.Embed(
      title=user.name,
      description=user.id,
      color=defaultColor
    )

    for name, val in infoFields.items():
      serverInfoEmbed.add_field(
        name=name,
        value=val,
        inline=infoFieldsInline[name]
      )

    serverInfoEmbed.set_author(**embedAuthor)
    serverInfoEmbed.timestamp = datetime.datetime.utcnow()
    serverInfoEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
    serverInfoEmbed.set_thumbnail(url=user.avatar_url)

    await ctx.send(embed=serverInfoEmbed)

def setup(bot):
  bot.add_cog(info(bot))