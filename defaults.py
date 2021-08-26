import discord
import datetime

class defaults():
  color = 0xe6847b

  spotifyColor = 0x1DB954

  guildIDs = [694470208315719750, 878002011965108235]

  timestamp = datetime.datetime.utcnow()

  dbKeys = {
    "nsfwStats": {},
    "currentStatus": 0
  }

  statusList = [
    "with Patser",
    "with my milkers",
    "Africa Simulator 2021 Deluxe Edition",
    "with Tropic\'s fat ass",
    "Roark\'s Attack on Titan Fan Game",
    "with BBC"
  ]

  rainbowColors = [
      0xff0000,
      0xff7f00,
      0xffff00,
      0x00ff00,
      0x0000ff,
      0x2e2b6f,
      0x8b00ff
    ]

  markdownChars = [
    "*",
    "_"
  ]

  sfwCategories = [
    "waifu",
    "neko",
    "dance",
    "cuddle",
    "cry",
    "hug",
    "kiss",
    "lick",
    "pat",
    "smug"
  ]

  nsfwCategories = [
    "waifu",
    "neko",
    "trap",
    "blowjob"
  ]

  def footer(user: discord.Member):
    return {
      "text": str(user),
      "icon_url": user.avatar_url
    }