import discord
from discord.ext import commands, tasks
import requests
import json
from functions import embedAuthor
import datetime

class dogelore(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.postDogeLore.start()

  @tasks.loop(minutes=30.0)
  async def postDogeLore(self):
    while True:
      data = requests.get("https://reddit-meme-api.herokuapp.com/dogelore/")
      jsonData = json.loads(data.text)

      title = jsonData["title"]
      author = jsonData["author"]
      imgUrl = jsonData["url"]
      upvotes = int(jsonData["ups"])
      postUrl = jsonData["post_link"]

      if upvotes > 50:
        break
    
    chars = [char for char in author]
    
    for char in chars:
      if char in ["*", "_"]:
        chars.insert(chars.index(char), "\\")

    author = "".join(chars)

    dogeLoreEmbed = discord.Embed(
      title=title,
      url=postUrl,
      description=f"u/{author}\n\nUpvotes: `{upvotes}`",
      color=0xCB9800
    )

    dogeLoreEmbed.set_author(**embedAuthor)
    dogeLoreEmbed.timestamp = datetime.datetime.utcnow()

    splittedUrl = imgUrl.split(".")

    if splittedUrl[len(splittedUrl) - 1] in ["jpg", "jpeg", "png"]:
      dogeLoreEmbed.set_image(url=imgUrl)
      await self.bot.get_channel(840010646464888832).send(embed=dogeLoreEmbed)
    
    else:
      await self.bot.get_channel(840010646464888832).send(embed=dogeLoreEmbed)
      await self.bot.get_channel(840010646464888832).send(imgUrl)

def setup(bot):
  bot.add_cog(dogelore(bot))