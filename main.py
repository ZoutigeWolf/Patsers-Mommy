import discord
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import CheckFailure, has_permissions
import os
from replit import db
from helpEmbeds import helpEmbeds, helpDefault
from functions import updateDictDB

intents = discord.Intents.default()
intents.members = True
intents.bans = True

bot = commands.Bot(
  command_prefix="s!",
  help_command=None,
  case_insensitive=True,
  intents=intents
)

defaultColor = 0xDC696B
embedAuthor = {
  "name": "Sumi",
  "icon_url": "https://cdn.discordapp.com/attachments/814146826214965271/834453090207137872/de7cg0p-e2dcc2c3-b548-4c51-808e-b44efc8ca690_2.png"
}

dbItems = {"nsfw": False, "defaultRole": None, "welcomeMessage": {"channel": None, "message": None}}

@bot.event
async def on_ready():
  print(f"Bot started ({bot.user})")
  await bot.change_presence(activity=discord.Game(name="with Kazuya"))

  for guild in bot.guilds:
    guildDB = db[str(guild.id)]
    for item in dbItems:
      if item not in guildDB:
        await updateDictDB(guild.id, item, dbItems[item])

  bot.load_extension("cogs.nsfw")
  bot.load_extension("cogs.moderation")
  bot.load_extension("cogs.config")
  bot.load_extension("cogs.fun")
  bot.load_extension("cogs.info")
  print("cogs loaded")
  print(db["694470208315719750"])

@bot.event
async def on_guild_join(guild):
  await updateDictDB(guild.id, "nsfw", False)
  await updateDictDB(guild.id, "defaultRole", None)
  await updateDictDB(guild.id, "welcomeMessage", None)
  await updateDictDB(guild.id, "welcomeChannel", None)

@bot.event
async def on_member_join(member):
  welcomeMessageDict = {
    "{name}": member.display_name,
    "{mention}": member.mention,
    "{fullname}" : member,
    "{membercount}": member.guild.member_count,
  }

  guildDB = db[str(member.guild.id)]
  role = guildDB["defaultRole"]

  welcomeChannel = guildDB["welcomeChannel"]
  welcomeMessage = guildDB["welcomeMessage"]
  
  if role:
    await member.add_roles(get(member.guild.roles, id=role))

  if welcomeChannel is not None and welcomeMessage is not None:
    channel = bot.get_channel(welcomeChannel)

    for word in welcomeMessageDict:
      welcomeMessage = welcomeMessage.replace(word, str(welcomeMessageDict[word]))

    await channel.send(welcomeMessage)

@bot.command()
async def help(ctx, cat=None):
  if cat:
    helpEmbed = helpEmbeds[cat]
  else:
    helpEmbed = helpDefault

  helpEmbed.set_footer(text=ctx.author)
  await ctx.send(embed=helpEmbed)

@bot.command()
async def invite(ctx):
  await ctx.send(f"You can invite me to your server here: <https://discord.com/api/oauth2/authorize?client_id=834343947694243860&permissions=8&scope=bot>")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You don't have the permissions required for this command")

  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("You need to fill out all the necessary arguments")

bot.run(os.environ['TOKEN'])