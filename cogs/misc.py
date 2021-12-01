import discord
from discord import Spotify
from discord.utils import get
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

import random
import requests
import json
import datetime

class Misc(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @cog_ext.cog_slash(
    name="kiss",
    description="Kiss someone 😘",
    options = [
      create_option(
        name="user",
        description="User that you want to kiss",
        option_type=6,
        required=True
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def _kiss(self, ctx: SlashContext, user: discord.Member):
    await ctx.defer()

    if ctx.author == user:
      await ctx.send("You can't kiss yourself virgin")

    else:
      kissEmbed = discord.Embed(
        description=f"{ctx.author.mention} kissed {user.mention}",
        color=defaults.color
      )

      kissEmbed.set_image(url="https://static.wikia.nocookie.net/the-weeb-squad/images/b/b8/Ca_8Vdjo_400x400.jpg/revision/latest?cb=20180416021709")

      await ctx.send(embed=kissEmbed)


  @cog_ext.cog_subcommand(
    base="meter",
    name="gay",
    description="Gay % calculator",
    options = [
      create_option(
        name="user",
        description="The user to calculate",
        option_type=6,
        required=False
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def meter_gay(self, ctx: SlashContext, user: discord.Member=None):
    await ctx.defer()

    user = user if user else ctx.author

    calcEmbed = discord.Embed(
      description=f"{user.mention} is {random.randint(0, 100)}% gay",
      color=random.choice(defaults.rainbowColors)
    )

    await ctx.send(embed=calcEmbed)

  @cog_ext.cog_subcommand(
    base="http",
    name="cat",
    description="Get an HTPP cat",
    options = [
      create_option(
        name="code",
        description="HTTP Response code",
        option_type=4,
        required=True
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def http_cat(self, ctx: SlashContext, code):
    await ctx.defer()

    httpEmbed = discord.Embed(
      title=f"HTTP code `{code}`",
      color=defaults.color
    )

    httpEmbed.set_image(url=f"https://http.cat/{code}.jpg")

    await ctx.send(embed=httpEmbed)

  @cog_ext.cog_subcommand(
    base="http",
    name="indian",
    description="Get an HTTP indian",
    options = [
      create_option(
        name="code",
        description="HTTP Response code",
        option_type=4,
        required=True
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def http_indian(self, ctx: SlashContext, code):
    await ctx.defer()

    r = requests.get(f"https://vadivelu.anoram.com/gif/{code}.gif")
    if r.status_code != 404:
      url = f"https://vadivelu.anoram.com/gif/{code}.gif"

    else:
      r = requests.get(f"https://vadivelu.anoram.com/jpg/{code}.jpg")
      if r.status_code != 404:
        url = f"https://vadivelu.anoram.com/jpg/{code}.jpg"

      else:
        url = "https://vadivelu.anoram.com/gif/404.gif"

    httpEmbed = discord.Embed(
      title=f"HTTP code `{code}`",
      color=defaults.color
    )

    if url == "https://vadivelu.anoram.com/gif/404.gif":
      httpEmbed.description = "Code not found"

    httpEmbed.set_image(url=url)

    await ctx.send(embed=httpEmbed)

  @cog_ext.cog_subcommand(
    base="anime",
    name="quote",
    description="Random anime quote",
    guild_ids=defaults.guildIDs
  )
  async def anime_quote(self, ctx: SlashContext):
    await ctx.defer()

    r = requests.get("https://animechan.vercel.app/api/random")
    data = json.loads(r.text)

    quote = list(data["quote"])

    for i, char in enumerate(quote):
      if char in defaults.markdownChars:
        quote.insert(i, "\\")

    quote = "".join(quote)

    quoteEmbed = discord.Embed(
      title=f"*\"{quote}\"*",
      description=f"- {data['character']}",
      color=defaults.color
    )

    quoteEmbed.add_field(
      name="Anime",
      value=data["anime"],
      inline=False
    )

    await ctx.send(embed=quoteEmbed)

  @cog_ext.cog_subcommand(
    base="anime",
    name="sfw",
    subcommand_group="waifu",
    description="Random anime waifu",
    options = [
      create_option(
        name="category",
        description="Waifu category",
        option_type=3,
        required=True,
        choices = [create_choice(name=cat, value=cat) for cat in defaults.sfwCategories]
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def anime_waifu_sfw(self, ctx: SlashContext, category):
    await ctx.defer()

    r = requests.get(f"https://api.waifu.pics/sfw/{category}")
    data = json.loads(r.text)

    waifuEmbed = discord.Embed(
      title=f"SFW | `{category}`",
      color=defaults.color
    )

    waifuEmbed.set_image(url=data["url"])

    await ctx.send(embed=waifuEmbed)

  @cog_ext.cog_subcommand(
    base="anime",
    name="nsfw",
    subcommand_group="waifu",
    description="Random anime waifu",
    options = [
      create_option(
        name="category",
        description="Waifu category",
        option_type=3,
        required=True,
        choices = [create_choice(name=cat, value=cat) for cat in defaults.nsfwCategories]
      )
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.is_nsfw()
  async def anime_waifu_nsfw(self, ctx: SlashContext, category):
    await ctx.defer()

    r = requests.get(f"https://api.waifu.pics/nsfw/{category}")
    data = json.loads(r.text)

    waifuEmbed = discord.Embed(
      title=f"NSFW | `{category}`",
      color=defaults.color
    )

    waifuEmbed.set_image(url=data["url"])

    await ctx.send(embed=waifuEmbed)

  @cog_ext.cog_slash(
    name="advice",
    description="Get advice",
    guild_ids=defaults.guildIDs
  )
  async def _advice(self, ctx: SlashContext):
    await ctx.defer()

    r = requests.get("https://api.adviceslip.com/advice")
    data = json.loads(r.text)

    adviceEmbed = discord.Embed(
      title=data["slip"]["advice"],
      color=defaults.color
    )

    await ctx.send(embed=adviceEmbed)

  @cog_ext.cog_slash(
    name="kanyequote",
    description="Random Kanye quote",
    guild_ids=defaults.guildIDs
  )
  async def _kanyequote(self, ctx: SlashContext):
    await ctx.defer()

    r = requests.get("https://api.kanye.rest/")
    quote = json.loads(r.text)["quote"]

    quoteEmbed = discord.Embed(
      title=f"*\"{quote}\"*",
      color=defaults.color
    )

    await ctx.send(embed=quoteEmbed)

  @cog_ext.cog_subcommand(
    base="spotify",
    name="user",
    description="Info about the song a user is listening to",
    options = [
      create_option(
        name="user",
        description="The user to get the data from",
        option_type=6,
        required=False
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def spotify_user(self, ctx: SlashContext, user: discord.Member=None):
    await ctx.defer()

    user = user if user else discord.utils.get(ctx.guild.members, id=ctx.author.id)

    activity = None

    for act in user.activities:
      if isinstance(act, Spotify):
        activity = act
        break

    if activity:
      song = activity

      spotifyEmbed = discord.Embed(
        title=song.title,
        description=song.artist,
        url=f"https://open.spotify.com/track/{song.track_id}",
        color=defaults.spotifyColor
      )

      spotifyEmbed.set_author(name=f"{user.name} is listening to:", icon_url=user.avatar_url)
      spotifyEmbed.set_thumbnail(url=song.album_cover_url)
      
      def getTime(t):
        m, s = divmod(t.seconds, 60)
        s = s if s >= 10 else f"0{s}"
        return [m, s]

      def mapVal(x, inMin, inMax, outMin, outMax):
        return int((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin)

      def getBar(start, end, current):
        totSec = (end - start).seconds
        currSec = (current - start).seconds

        cVal = mapVal(currSec, 0, totSec, 0, 100)

        bar = []

        for i in range(0, 101, 5):
          if i <= cVal <= i + 4:
            bar.append("⬤")
            continue

          if i < cVal:
            bar.append("=")
            continue
          
          bar.append("-")
        
        return "".join(bar)

      start = song.created_at
      end = song.end
      current = datetime.datetime.now()

      elapsed = getTime(current - start)

      songDuration = getTime(song.duration)

      spotifyEmbed.add_field(
        name="Album",
        value=song.album,
        inline=False
      )

      spotifyEmbed.set_footer(text=f"{elapsed[0]}:{elapsed[1]} {getBar(start, end, current)} {songDuration[0]}:{songDuration[1]}")

      await ctx.send(embed=spotifyEmbed)

    else:
      await ctx.send(f"**{user.display_name}** isn't listening to spotfiy right now")

  @cog_ext.cog_subcommand(
    base="spotify",
    name="server",
    description="Every user who is listening to spotify in the server",
    guild_ids=defaults.guildIDs
  )
  async def spotify_server(self, ctx: SlashContext):
    await ctx.defer()

    guild = get(self.bot.guilds, id=ctx.guild.id)

    actList = {}

    for user in guild.members:
      for act in user.activities:
        if isinstance(act, Spotify):
          actList[user.id] = [act.title, act.artist, act.track_id]
          break

    actList = [f"**{i + 1}**. {get(guild.members, id=userID).mention} [{data[1]} - {data[0]}](https://open.spotify.com/track/{data[2]})" for i, (userID, data) in enumerate(actList.items())]
    
    n = len(actList)

    actList = "\n".join(actList)

    spotifyEmbed = discord.Embed(
      title=f"{n} {'user' if n == 1 else 'users'} are listening to Spotify",
      description=actList if actList else "No one is listening...",
      color=defaults.spotifyColor
    )

    await ctx.send(embed=spotifyEmbed)

  async def colorInfo(self, ctx, colorFormat, colorCode):
    r = requests.get(f"https://www.thecolorapi.com/id?{colorFormat}={colorCode}")
    data = json.loads(r.text)

    colorEmbed = discord.Embed(
      title=data["name"]["value"],
      color=int(data["hex"]["clean"], 16),
      url=f"https://www.thecolorapi.com/id?format=html&hex={data['hex']['clean']}"
    )

    colorEmbed.add_field(
      name="Hex",
      value=f"`{data['hex']['value']}`",
      inline=True
    )

    rgb = data["rgb"]
    hsl = data["hsl"]
    hsv = data["hsv"]
    cmyk = data["cmyk"]

    colorEmbed.add_field(
      name="RGB",
      value=f"`{rgb['r']}`, `{rgb['g']}`, `{rgb['b']}`",
      inline=True
    )

    colorEmbed.add_field(
      name="HSL",
      value=f"`{hsl['h']}`, `{hsl['s']}%`, `{hsl['l']}%`",
      inline=True
    )

    colorEmbed.add_field(
      name="HSV",
      value=f"`{hsv['h']}`, `{hsv['s']}%`, `{hsv['v']}%`",
      inline=True
    )

    colorEmbed.add_field(
      name="CMYK",
      value=f"`{cmyk['c']}`, `{cmyk['m']}`, `{cmyk['y']}`, `{cmyk['k']}`",
      inline=True
    )

    colorEmbed.set_image(url=f"https://dummyimage.com/200x200/{data['hex']['clean']}/ffffff.png&text=+")

    await ctx.send(embed=colorEmbed)

  @cog_ext.cog_subcommand(
    base="color",
    name="hex",
    description="Information about a color",
    options = [
      create_option(
        name="code",
        description="HEX color code",
        option_type=3,
        required=True,
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def color_hex(self, ctx: SlashContext, code):
    await ctx.defer()
    if "#" in code:
      code = code.replace("#", "")

    await self.colorInfo(ctx, "hex", code)

  @cog_ext.cog_subcommand(
    base="color",
    name="rgb",
    description="Information about a color",
    options = [
      create_option(
        name="r",
        description="Red",
        option_type=4,
        required=True,
      ),
      create_option(
        name="g",
        description="Green",
        option_type=4,
        required=True,
      ),
      create_option(
        name="b",
        description="Blue",
        option_type=4,
        required=True,
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def color_rgb(self, ctx: SlashContext, r, g, b):
    await ctx.defer()
    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
      code = f"{r},{g},{b}"
      await self.colorInfo(ctx, "rgb", code)

  @cog_ext.cog_subcommand(
    base="voice",
    name="user",
    description="Info about a user's voice activity",
    options = [
      create_option(
        name="user",
        description="The user to get the data from",
        option_type=6,
        required=False
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def voice_user(self, ctx: SlashContext, user: discord.Member=None):
    await ctx.defer()

    user =  user if user else ctx.author
    voice = user.voice

    def getMemberList(members):
      memberList = []

      for i, member in enumerate(members):
        if i < 10:
          memberList.append(f"**{i + 1}**. {member.mention}")

        else:
          memberList.append(f"{len(members) - 10} more...")
          break

      return memberList

    if voice:
      voiceEmbed = discord.Embed(
        title=voice.channel.name,
        color=defaults.color
      )

      voiceEmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

      voiceEmbed.add_field(
        name="Muted",
        value="Yes" if voice.mute or voice.self_mute else "No",
        inline=True
      )

      voiceEmbed.add_field(
        name="Deafend",
        value="Yes" if voice.deaf or voice.self_deaf else "No",
        inline=True
      )

      voiceEmbed.add_field(
        name="Streaming video",
        value="Yes" if voice.self_video else "No",
        inline=True
      )

      voiceEmbed.add_field(
        name="Streaming screen",
        value="Yes" if voice.self_stream else "No",
        inline=True
      )

      voiceEmbed.add_field(
        name="AFK",
        value="Yes" if voice.afk else "No",
        inline=True
      )

      voiceEmbed.add_field(
        name=f"Users in channel ({len(voice.channel.members)})",
        value="\n".join(getMemberList(voice.channel.members)),
        inline=False
      )

    else:
      voiceEmbed = discord.Embed(
        description=f"{user} is not in a voice channel",
        color=defaults.color
      )

    await ctx.send(embed=voiceEmbed)

def setup(bot):
  bot.add_cog(Misc(bot))