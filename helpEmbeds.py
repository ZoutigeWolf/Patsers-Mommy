import discord
import datetime

defaultColor = 0xDC696B
embedAuthor = {"name": "Sumi", "icon_url": "https://cdn.discordapp.com/attachments/814146826214965271/834453090207137872/de7cg0p-e2dcc2c3-b548-4c51-808e-b44efc8ca690_2.png"}

helpDefault = discord.Embed(
  title="Help Menu",
  description="""
  Prefix = s!

  <> = Required argument
  [] = Optional argument

  `help [category]`

  `help` | Main help menu
  ┡`nsfw` | NSFW commands
  ┡`moderation` | Moderation commands
  ┡`config` | Configurable settings
  ┖`misc` | Misc commands 
  `invite` | Get a link to invite the bot

  [Invite the bot](https://discord.com/api/oauth2/authorize?client_id=834343947694243860&permissions=8&scope=bot)
  """,
  color=defaultColor
)

helpDefault.set_author(**embedAuthor)
helpDefault.timestamp = datetime.datetime.utcnow() 

helpEmbeds = {}

helpEmbeds["nsfw"] = discord.Embed(
  title="NSFW Commands",
  description="""
  `r34 <tag>` | Get NSFW content from rule34.xxx
  """,
  color=defaultColor
)

helpEmbeds["nsfw"].set_author(**embedAuthor)


helpEmbeds["moderation"] = discord.Embed(
  title="Moderation Commands",
  description="""
  These commands are only available to staff members

  `ban <user> [reason]` | Ban someone from the server
  `kick <user> [reason]` | Kick someone from the server

  `role <option> <role> <setting>` | Change a role
  ┡`role give <role> <user>` | Give a role to a user
  ┡`role remove <role> <user>` | Remove a role from a user
  ┡`role color <role> <color>` | Change the color of a role
  ┖`role name <role> <name>` | Change the name of a color
  """,
  color=defaultColor
)

helpEmbeds["moderation"].set_author(**embedAuthor)
helpEmbeds["moderation"].timestamp = datetime.datetime.utcnow()

helpEmbeds["config"] = discord.Embed(
  title="Setting Commands",
  description="""
  These commands are only available to staff members

  `config [setting] [value]`

  `config` | Main command to change settings
  ┡`nsfw [True / False]` | Enable or disable nsfw content
  ┖`defaultrole [roleID / None]` | Set the default role users get automatically on join
  """,
  color=defaultColor
)

helpEmbeds["config"].set_author(**embedAuthor)
helpEmbeds["config"].timestamp = datetime.datetime.utcnow()  