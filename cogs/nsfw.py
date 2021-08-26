import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

import requests
import json
import random
import datetime
import math
import os

from replit import db
from collections import OrderedDict
from xml.dom import minidom

class NSFW(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  def register(self, user: discord.Member, tag):
    if str(user.id) in db["nsfwStats"]:
      db["nsfwStats"][str(user.id)]["amount"] += 1


      if tag in db["nsfwStats"][str(user.id)]["tags"]:
        db["nsfwStats"][str(user.id)]["tags"][tag] += 1

      else:
        db["nsfwStats"][str(user.id)]["tags"][tag] = 1

    else:
      defaultFormat = {
        "amount": 1,
        "tags": {tag: 1}
      }

      db["nsfwStats"][str(user.id)] = defaultFormat

  @cog_ext.cog_subcommand(
    base="r34",
    name="search",
    description="Get an image from rule34.xxx",
    options = [
      create_option(
        name="tag",
        description="A Rule34 tag",
        option_type=3,
        required=True
      )
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.is_nsfw()
  async def r34_search(self, ctx: SlashContext, tag):
    await ctx.defer()

    r = requests.get(f"https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={tag}")

    with open("r34.xml", "wb") as xmlFile:
      xmlFile.write(r.content)

    doc = minidom.parse("r34.xml")
    posts = doc.getElementsByTagName("post")

    postN = random.randint(0, len(posts) - 1)

    fileURL = posts[postN].attributes["file_url"].value

    isVideo = fileURL[:-4] == ".mp4"

    r34Embed = discord.Embed(
      title=fileURL,
      url=fileURL,
      color=defaults.color
    )

    r34Embed.set_footer(**defaults.footer(ctx.author))
    r34Embed.timestamp = datetime.datetime.utcnow()

    if not isVideo:
      r34Embed.set_image(url=fileURL)
    
    self.register(ctx.author, tag)

    await ctx.send(embed=r34Embed)

    if isVideo:
      await ctx.send(fileURL)

    os.remove("r34.xml")

  @cog_ext.cog_subcommand(
    base="r34",
    name="stats",
    description="See someone's NSFW search stats",
    options = [
      create_option(
        name="user",
        description="User to get the stats for (Leave blank to see your own stats)",
        option_type=6,
        required=False
      ),
      create_option(
        name="page",
        description="Stats page number (Leave blank for page 1)",
        option_type=4,
        required=False
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def r34_stats(self, ctx: SlashContext, user: discord.Member=None, page=1):
    await ctx.defer()

    user = user if user else ctx.author
    
    if str(user.id) in db["nsfwStats"].keys():
      stats = db["nsfwStats"][str(user.id)]
      
      amount = stats["amount"]
      tags = stats["tags"]
      
      tagsCount = OrderedDict(sorted(tags.items(), key=lambda kv: kv[1]))
      
      tagsListRaw = [f"**{i + 1}**. `{tag}`: searched `{count}` {'time' if count == 1 else 'times'}" for i, (tag, count) in enumerate(reversed(tagsCount.items()))]
      
      totalPages = math.ceil(len(tagsListRaw) / 10)
      
      if 1 <= page <= totalPages:
        startIndex = page * 10 - 10
        stopIndex = startIndex + 9

        tagsList = "\n".join([line for i, line in enumerate(tagsListRaw) if startIndex <= i <= stopIndex])
        
        statEmbed = discord.Embed(
          description=f"""
          Total searches: `{amount}`

          {tagsList}

          Page {page} / {totalPages}
          """,
          color=defaults.color
        )

        statEmbed.set_author(name=f"{user}'s NSFW stats", icon_url=user.avatar_url)
        statEmbed.set_footer(**defaults.footer(ctx.author))
        statEmbed.timestamp = datetime.datetime.utcnow()
        
        await ctx.send(embed=statEmbed)

      else:
        await ctx.send("Invalid page number")

    else:
      await ctx.send(f"Couldn't find **{user}** in the database\nTry `/r34 search` first")

def setup(bot):
  bot.add_cog(NSFW(bot))