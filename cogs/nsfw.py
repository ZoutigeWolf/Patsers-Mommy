import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure, has_permissions
from replit import db
import json
import requests
import random

class nsfw(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def r34(self, ctx, search):
    nsfwDB = db[str(ctx.guild.id)]
    if nsfwDB["nsfw"]:
      if ctx.channel.is_nsfw():
        data = requests.get(f"https://r34-json-api.herokuapp.com/posts?tags={search}")
        dataList = json.loads(data.text)
        fileUrl = dataList[random.randint(0, len(dataList) - 1)]["file_url"]

        await ctx.send(fileUrl)

      else:
        await ctx.send("This isn't an NSFW channel!")

    else:
      await ctx.send("NSFW is disabled in this server!")

def setup(bot):
  bot.add_cog(nsfw(bot))