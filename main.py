import discord
from discord.utils import get
from discord.ext import commands, tasks
from discord_slash import SlashCommand
from discord_components import DiscordComponents

from defaults import defaults

import os
import collections

from flask import Flask, render_template, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

from threading import Thread
from replit import db

bot = commands.Bot(
  command_prefix="p!",
  intents=discord.Intents.all(),
  help_command=None
)

slash = SlashCommand(
  bot,
  sync_commands=True,
)
@tasks.loop(seconds=30.0)
async def switchStatus():
  if db["currentStatus"] < len(defaults.statusList) - 1:
    db["currentStatus"] += 1
  
  else:
    db["currentStatus"] = 0

  status = defaults.statusList[db["currentStatus"]]

  await bot.change_presence(
    status=discord.Status.online,
    activity=discord.Game(status)
  )

@bot.event
async def on_ready():
  DiscordComponents(bot) 
  print(f"Bot started ({bot.user})")
  switchStatus.start()

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")
    print(f"Loaded cog {filename[:-3]}")

for k, v in defaults.dbKeys.items():
  if k not in db.keys():
    db[k] = v

@bot.event
async def on_member_join(user):
  guild = user.guild
  channel = guild.system_channel

  if guild.id == 694470208315719750:
    role = get(guild.roles, id=694471837236723743)
    await user.add_roles(role)

  await channel.send(f"Welcome to *{guild.name}* {user.mention}!")

@bot.event
async def on_slash_command_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send(f"You need the permission **{''.join(error.missing_perms)}** to use this command")

  elif isinstance(error, commands.NotOwner):
    await ctx.send("You have to be the bot owner to use this command")

  elif isinstance(error, commands.MissingRole):
    await ctx.send(f"You need the role **{error}** to use this command")

  elif isinstance(error, commands.NSFWChannelRequired):
    await ctx.send("This command can only be used in NSFW channels")

  else:
    await ctx.send("An error occured")

  print(f"ERROR >> {ctx.author} >> {error}")

def getUserData(user: discord.Member):
  return [str(user), user.avatar_url]

def getNsfwStats():
  data = db["nsfwStats"]

  allData = {}

  for userID, userData in data.items():
    for tag, i in userData["tags"].items():
      if tag in allData.keys():
        allData[tag] += i

      else:
        allData[tag] = i

  tagsData = collections.OrderedDict(sorted(allData.items(), key=lambda kv: kv[1]))

  tagsList = reversed([[tag, i] for tag, i in tagsData.items()])

  return tagsList

def getNsfwUserStats(userID):
  data = db["nsfwStats"][str(userID)]

  totalN = data["amount"]

  tagsData = collections.OrderedDict(sorted(data["tags"].items(), key=lambda kv: kv[1]))

  tagsList = reversed([[tag, i] for tag, i in tagsData.items()])

  return [totalN, tagsList]

def getUserProfile(userID):
  guild = get(bot.guilds, id=694470208315719750)
  user = get(guild.members, id=userID)

  roleList = [[str(role.color), role.name] for role in reversed(user.roles) if role.name != "@everyone"]

  return [roleList]

app = Flask(
  __name__,
  template_folder="site/html",
  static_folder="site/static"
)

app.secret_key = os.environ["APP_SECRET"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["DISCORD_CLIENT_ID"] = os.environ["CLIENT_ID"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["CLIENT_SECRET"]
app.config["DISCORD_REDIRECT_URI"] = "https://patsers-mommy.zoutigewolf.repl.co/callback/"
app.config["DISCORD_BOT_TOKEN"] = os.environ["TOKEN"]

discordAuth = DiscordOAuth2Session(app)

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
  return redirect(url_for("login"))

@app.route("/")
def home():
  loggedIn = discordAuth.authorized

  if loggedIn:
    user = discordAuth.fetch_user()
    return render_template("home.html", loggedIn=loggedIn, avatar=user.avatar_url, name=str(user))

  return render_template("home.html", loggedIn=loggedIn)

@app.route("/stats/")
def stats():
  loggedIn = discordAuth.authorized
  if loggedIn:
    user = discordAuth.fetch_user()
    return render_template("stats.html", loggedIn=loggedIn, stats=getNsfwStats(), userStats=getNsfwUserStats(user.id), avatar=user.avatar_url, name=str(user))

  return render_template("stats.html", loggedIn=loggedIn, stats=getNsfwStats())
@app.route("/dashboard/")
@requires_authorization
def dashboard():
  loggedIn = discordAuth.authorized
  user = discordAuth.fetch_user()
  if user.id == 298516275322290188:
    return render_template("dashboard.html", loggedIn=loggedIn, avatar=user.avatar_url, name=str(user))

  return render_template("invalidDashboard.html", loggedIn=loggedIn, avatar=user.avatar_url, name=str(user))

@app.route("/profile/")
@requires_authorization
def profile():
  loggedIn = discordAuth.authorized
  user = discordAuth.fetch_user()
  return render_template("profile.html", loggedIn=loggedIn, profile=getUserProfile(user.id), avatar=user.avatar_url, name=str(user))

@app.route("/callback/")
def callback():
  discordAuth.callback()
  loggedIn = discordAuth.authorized
  if loggedIn:
    user = discordAuth.fetch_user()
    return render_template("home.html", loggedIn=loggedIn, avatar=user.avatar_url, name=str(user))

@app.route("/login/")
def login():
  return discordAuth.create_session(scope=["identify", "guilds"])

@app.route("/logout/")
def logout():
  discordAuth.revoke()
  return redirect(url_for("home"))

def startSite():
  app.run(host="0.0.0.0", port=8080)

def runSite():
  t = Thread(target=startSite)
  t.start()

runSite()
bot.run(os.environ["TOKEN"])