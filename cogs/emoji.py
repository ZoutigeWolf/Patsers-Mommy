import discord
from discord.ext import commands
from discord.utils import get
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

import requests
import os

class Emoji(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_subcommand(
    base="emoji",
    name="add",
    description="Add an emoji",
    options = [
      create_option(
        name="name",
        description="The name of the emoji you want to add",
        option_type=3,
        required=True,
      ),
      create_option(
        name="image_url",
        description="The image URL for the emoji you want to add",
        option_type=3,
        required=True
      )
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.has_permissions(manage_emojis=True)
  async def emoji_add(self, ctx: SlashContext, name, image_url):
    await ctx.defer()

    guild = get(self.bot.guilds, id=ctx.guild.id)
    guildEmojis = [emoji.name for emoji in ctx.guild.emojis]

    if name not in guildEmojis:
      r = requests.get(image_url)

      imgFile = open("emojiImg.png", "wb")
      imgFile.write(r.content)
      imgFile.close()

      newEmoji = await guild.create_custom_emoji(  
        name=name,
        image=open("emojiImg.png", "rb").read(),
        reason=f"{ctx.author} created the emoji {name}"
      )

      await ctx.send(f"Created the emoji `{name}`\n{newEmoji.url}")

      imgFile.close()
      os.remove("emojiImg.png")

    else:
      await ctx.send("That emoji name already exists")

  @cog_ext.cog_subcommand(
    base="emoji",
    name="delete",
    description="Delete an emoji",
    options = [
      create_option(
        name="name",
        description="The name of the emoji you want to delete",
        option_type=3,
        required=True
      )
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.has_permissions(manage_emojis=True)
  async def emoji_delete(self, ctx: SlashContext, name):
    guild = get(self.bot.guilds, id=ctx.guild.id)

    emoji = get(guild.emojis, name=name)

    if emoji:
      await emoji.delete(reason=f"{ctx.author} deleted the emoji {emoji.name}")

      await ctx.send(f"Deleted the emoji `{emoji.name}`")

    else:
      await ctx.send("That emoji doesn't exist")

  @cog_ext.cog_subcommand(
    base="emoji",
    name="edit",
    description="Edit an emoji's name",
    options = [
      create_option(
        name="emoji_name",
        description="The name of the emoji you want to edit",
        option_type=3,
        required=True
      ),
      create_option(
        name="new_name",
        description="The new name for the emoji",
        option_type=3,
        required=True
      )
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.has_permissions(manage_emojis=True)
  async def emoji_edit(self, ctx: SlashContext, emoji_name, new_name):
    guild = get(self.bot.guilds, id=ctx.guild.id)

    emoji = get(guild.emojis, name=emoji_name)

    if emoji:
      await emoji.edit(
        name=new_name,
        reason=f"{ctx.author} set the name from {emoji.name} to {new_name}"
      )

      await ctx.send(f"Set the name of the emoji `{emoji_name}` to `{new_name}`")

    else:
      await ctx.send("That emoji doesn't exist")

def setup(bot):
  bot.add_cog(Emoji(bot))