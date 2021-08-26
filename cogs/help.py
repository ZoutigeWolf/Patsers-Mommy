import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @cog_ext.cog_slash(
    name="help",
    description="Help menu",
    options=[
      create_option(
        name="category",
        description="Help for a specific category",
        option_type=3,
        required=True,
        choices=[
          create_choice(
            name="Moderation",
            value="Moderation"
          ),
          create_choice(
            name="Misc",
            value="Misc"
          ),
          create_choice(
            name="NSFW",
            value="NSFW"
          ),
          create_choice(
            name="Roles",
            value="Roles"
          )
        ]
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def _help(self, ctx: SlashContext, category):
    await ctx.defer()

    if category == "Moderation":
      description = """
      `ban` > Ban a user
      `kick` > Kick a user
      """

    elif category == "Misc":
      description = """
      `advice` > Get advice
      `kiss` > Kiss someone
      `meter gay` > Gay % calculator
      `http cat` > Get an HTTP cat
      `http indian` > Get an HTTP indian
      `starwars people` > Info about a Star Wars character
      `starwars planet` > Info about a Star Wars planet
      `starwars species` > Info about a Star Wars species
      `starwars starship` > Info about a Star Wars starship
      `starwars vehicle` > Info about a Star Wars vehicle
      `spotify user` > Info about someone's currently playing song
      `spotify server` > See everyone who is listening to spotify in the server
      `voice` > Info about someone's voice activity
      `color` > Info about a color
      `emoji` > Edit server emojis
      `anime waifu sfw` > Get a waifu
      `anime quote` > Get a random anime quote
      `kanyequote` > Random Kanye quote
      """

    elif category == "NSFW":
      description = """
      `r34 search` > Get an image from rule34.xxx
      `r34 stats` > See someone's r34 search stats
      `anime waifu nsfw` > Get a waifu (NSFW)
      """

    elif category == "Roles":
      description = """
      `role give` > Give a role to a user
      `role remove` > Remove a role from a user
      `role edit name` > Edit a role name
      `role edit color` > Edit a role color
      """

    helpEmbed = discord.Embed(
      title=f"{category} - Help",
      description=description,
      color=defaults.color
    )

    helpEmbed.set_footer(**defaults.footer(ctx.author))
    helpEmbed.timestamp = defaults.timestamp

    await ctx.send(embed=helpEmbed)

def setup(bot):
  bot.add_cog(Help(bot))