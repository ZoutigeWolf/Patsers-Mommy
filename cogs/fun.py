import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @has_permissions(manage_messages=True)
  async def sendmessage(self, ctx, channel: discord.TextChannel, tts: bool=False, *message):
    await channel.send(" ".join(message), tts=tts)
    
def setup(bot):
  bot.add_cog(fun(bot))