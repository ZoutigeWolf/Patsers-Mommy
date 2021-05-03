import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import has_permissions
from functions import updateDictDB, defaultColor, embedAuthor
from replit import db
import datetime

class config(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name="config", invoke_without_command=True)
  @has_permissions(manage_guild=True)
  async def config(self, ctx):
    configDict = db[str(ctx.guild.id)]
    configNsfw = configDict["nsfw"]
    configDefaultRole = get(ctx.guild.roles, id=configDict["defaultRole"])
    configWelcomeChannel = configDict["welcomeChannel"]
    configWelcomeMessage = configDict["welcomeMessage"]

    configEmbed = discord.Embed(
      title=f"Server config for {ctx.guild.name}",
      description=f"""
        You can change a setting with
        `s!config <setting> <value>`

        **NSFW**: {configNsfw}
        **Default Role**: {configDefaultRole.mention}
        **Welcome channel**: {get(ctx.guild.channels, id=configWelcomeChannel).mention}
        **Welcome message**: "{configWelcomeMessage}"
       """,
      color=defaultColor
    )

    configEmbed.set_author(**embedAuthor)
    configEmbed.timestamp = datetime.datetime.utcnow()
    configEmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=configEmbed)


  @config.command(name="nsfw")
  @has_permissions(manage_guild=True)
  async def nsfw_subcommand(self, ctx, settingValue=None):
    configDict = db[str(ctx.guild.id)]
    configNsfw = configDict["nsfw"]

    if settingValue is None:
      await ctx.send(f"**NSFW** is currently set to **{configNsfw}**")

    else:
      settingValue = settingValue.lower()
      if settingValue in ["true", "false"]:
        if settingValue == "true":
          settingValue = True

        elif settingValue == "false":
          settingValue = False
          
        await updateDictDB(str(ctx.guild.id), "nsfw", settingValue)
        await ctx.send(f"Set **NSFW** to **{settingValue}**")

      else:
        await ctx.send(f"**{settingValue}** isn't a valid setting for **NSFW**")

  @config.command(name="defaultrole")
  @has_permissions(manage_guild=True)
  async def defaultrole_subcommand(self, ctx, settingValue=None):
    configDict = db[str(ctx.guild.id)]
    configDefaultRole = get(ctx.guild.roles, id=configDict["defaultRole"])

    if settingValue is None:
      await ctx.send(f"The default role is currently set to **{configDefaultRole}**")

    else:
      roleID = int(settingValue)

      serverRoles = [role.id for role in ctx.guild.roles]

      if roleID in serverRoles:
        if get(ctx.guild.roles, id=roleID) < ctx.guild.self_role:
          await updateDictDB(str(ctx.guild.id), "defaultRole", roleID)
          await ctx.send(f"Set The default role to **{get(ctx.guild.roles, id=roleID)}**")
          
        else:
          await ctx.send(f"You can't set the role **{get(ctx.guild.roles, id=roleID)}** as the default role due to the role hierarchy")

      else:
        await ctx.send(f"I can't find a role with the ID **{roleID}**")

  @config.command(name="welcomechannel")
  @has_permissions(manage_guild=True)
  async def welcomechannel_subcommand(self, ctx, settingValue: discord.TextChannel=None):
    configDict = db[str(ctx.guild.id)]
    configWelcomeChannel = configDict["welcomeChannel"]

    if settingValue is None:
      await ctx.send(f"The welcome channel is currently set to **{get(ctx.guild.channels, id=configWelcomeChannel)}**")

    else:

      db[str(ctx.guild.id)]["welcomeChannel"] = settingValue.id

      await ctx.send(f"Set the welcome channel to **{settingValue}**")

  @config.command(name="welcomemessage")
  @has_permissions(manage_guild=True)
  async def welcomemessage_subcommand(self, ctx, *settingValue):
    configDict = db[str(ctx.guild.id)]
    configWelcomeMessage = configDict["welcomeMessage"]

    if not settingValue:
      await ctx.send(f"The welcome message is currently set to **{configWelcomeMessage}**")

    else:
      settingValue = " ".join(settingValue)
      db[str(ctx.guild.id)]["welcomeMessage"] = settingValue
      await ctx.send(f"Set the welcome message to **{settingValue}**")

def setup(bot):
  bot.add_cog(config(bot))