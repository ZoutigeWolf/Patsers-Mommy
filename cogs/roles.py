import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

class Roles(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @cog_ext.cog_subcommand(
    base="role",
    name="give",
    description="Give a role to a user",
    base_description="Edit roles",
    options=[
      create_option(
        name="role",
        description="The role to give",
        option_type=8,
        required=True
      ),
      create_option(
        name="user",
        description="The user to give the role to",
        option_type=6,
        required=True
      ),
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.has_permissions(manage_roles=True)
  async def role_give(self, ctx: SlashContext, role: discord.Role, user: discord.Member):
    await ctx.defer()
    
    if ctx.author.top_role > role:
      await user.add_roles(role)

      roleEmbed = discord.Embed(
        description=f"Gave the role {role.mention} to {user.mention}",
        color=role.color
      )

      await ctx.send(embed=roleEmbed)

    else:
      await ctx.send("You can't give that role due to the role hierarchy")

  @cog_ext.cog_subcommand(
    base="role",
    name="remove",
    description="Remove a role from a user",
    base_description="Edit roles",
    options=[
      create_option(
        name="role",
        description="The role to remove",
        option_type=8,
        required=True
      ),
      create_option(
        name="user",
        description="The user to remove the role from",
        option_type=6,
        required=True
      ),
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.has_permissions(manage_roles=True)
  async def role_remove(self, ctx: SlashContext, role: discord.Role, user: discord.Member):
    await ctx.defer()
    
    if ctx.author.top_role > role:
      await user.add_roles(role)

      roleEmbed = discord.Embed(
        description=f"Removed the role {role.mention} from {user.mention}",
        color=role.color
      )

      await ctx.send(embed=roleEmbed)

    else:
      await ctx.send("You can't remove that role due to the role hierarchy")

  @cog_ext.cog_subcommand(
    base="role",
    name="name",
    subcommand_group="edit",
    description="Edit a role name",
    subcommand_group_description="Edit a role",
    base_description="Edit roles",
    options=[
      create_option(
        name="role",
        description="The role to edit",
        option_type=8,
        required=True
      ),
      create_option(
        name="name",
        description="The new name for the role",
        option_type=3,
        required=True
      ),
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.has_permissions(manage_roles=True)
  async def role_edit_name(self, ctx: SlashContext, role: discord.Role, name):
    await ctx.defer()
    
    if ctx.author.top_role > role:
      oldName = role.name
      await role.edit(name=name)

      roleEmbed = discord.Embed(
        description=f"Set the name for the role **{oldName}** to **{name}**",
        color=role.color
      )

      await ctx.send(embed=roleEmbed)

    else:
      await ctx.send("You can't edit that role due to the role hierarchy")

  @cog_ext.cog_subcommand(
    base="role",
    name="color",
    subcommand_group="edit",
    description="Edit a role color",
    subcommand_group_description="Edit a role",
    base_description="Edit roles",
    options=[
      create_option(
        name="role",
        description="The role to edit",
        option_type=8,
        required=True
      ),
      create_option(
        name="color",
        description="The new color for the role",
        option_type=3,
        required=True
      ),
    ],
    guild_ids=defaults.guildIDs
  )
  @commands.has_permissions(manage_roles=True)
  async def role_edit_color(self, ctx: SlashContext, role: discord.Role, colorInput):
    await ctx.defer()

    color = colorInput

    if "#" in color:
      color = color.replace("#", "")
    
    if ctx.author.top_role > role:
      oldColor = role.color
      await role.edit(color=int(color, 16))

      roleEmbed = discord.Embed(
        description=f"Set the color for the role **{str(oldColor)}** to **{colorInput}**",
        color=int(color, 16)
      )

      await ctx.send(embed=roleEmbed)

    else:
      await ctx.send("You can't edit that role due to the role hierarchy")

def setup(bot):
  bot.add_cog(Roles(bot))