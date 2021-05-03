import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure, has_permissions
from replit import db

class moderation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @has_permissions(ban_members=True)
  async def ban(self, ctx, user: discord.Member, *reason):
    await ctx.guild.ban(user, reason=f"Banned by {ctx.author} | Reason: {reason}", delete_message_days=7)
    await ctx.send(f"Banned {user}")

  @commands.command()
  @has_permissions(kick_members=True)
  async def kick(self, ctx, user: discord.Member, *reason):
    await ctx.guild.kick(user, reason=f"Kicked by {ctx.author} | Reason: {reason}")
    await ctx.send(f"Kicked {user}")

  @commands.group(name="role", invoke_without_command=True)
  @has_permissions(manage_roles=True)
  async def role(self, ctx):
    await ctx.send("s!role <command> <value>")

  @role.command(name="give")
  @has_permissions(manage_roles=True)
  async def give_subcommand(self, ctx, role: discord.Role, user: discord.Member):
    if role < ctx.author.top_role:
      if role not in user.roles:
        await user.add_roles(role)
        await ctx.send(f"Gave the role **{role.name}** to **{user.display_name}**")

      else:
        await ctx.send(f"**{user.display_name}** already has the role **{role.name}**")

    else:
      await ctx.send("You can't give this role due to the role hierarchy")

  @role.command(name="remove")
  @has_permissions(manage_roles=True)
  async def remove_subcommand(self, ctx, role: discord.Role, user: discord.Member):
    if role < ctx.author.top_role:
      if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"Removed the role **{role.name}** from **{user.display_name}**")

      else:
        await ctx.send(f"**{user.display_name}** doesn't have the role **{role.name}**")

    else:
      await ctx.send("You can't remove this role due to the role hierarchy")

def setup(bot):
  bot.add_cog(moderation(bot))