import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from defaults import defaults

import random
import datetime
import requests
import json
import math
import difflib

from pygicord import Paginator

class StarWars(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  def getDataByName(self, objectType, query):
    i = 1
    while True:
      r = requests.get(f"https://swapi.dev/api/{objectType}/?page={i}")
      data = json.loads(r.text)

      for item in data["results"]:
        if item["name"].lower() == query.lower():
          return item

      pages =  math.ceil(data["count"] / 10)

      if i < pages:
        i += 1

      else:
        return None

  def getDataByURL(self, url):
    r = requests.get(url)
    return json.loads(r.text)

  def getMovieList(self, data):
    movies = data["films"]

    movieList = []

    for movie in movies:
      movData = self.getDataByURL(movie)

      movieList.append(f"Episode {movData['episode_id']}: {movData['title']}")

    return movieList

  def getPeopleList(self, data, name):
    people = data[name]

    peopleList = []

    for person in people:
      personData = self.getDataByURL(person)

      peopleList.append(f"{personData['name']}")

    if peopleList:
      return peopleList

    return ["n/a"]

  def getPaginator(self, objectType):
    pages = []

    page = 1

    while True:
      r = requests.get(f"https://swapi.dev/api/{objectType}/?page={page}")
      if r.status_code != 404:
        data = json.loads(r.text)["results"]

        items = "\n".join([item["name"] for item in data])

        totalPages = math.ceil(json.loads(r.text)["count"] / 10)

        pageEmbed = discord.Embed(
          title=f"Starwars {objectType}",
          description=f"""
          {items}

          {page} / {totalPages}
          """,
          color=defaults.color
        )

        pages.append(pageEmbed)

        page += 1

      else:
        break

    return pages

  @cog_ext.cog_subcommand(
    base="starwars",
    name="people",
    description="Get a person from Star Wars",
    options = [
      create_option(
        name="person",
        description="Person in Star Wars",
        option_type=3,
        required=False
      )
    ],
    guild_ids=defaults.guildIDs
  )
  async def starwars_people(self, ctx: SlashContext, person=None):
    await ctx.defer()

    objectType = "people"
    
    if person:
      data = self.getDataByName(objectType, person)

      if data:
        personEmbed = discord.Embed(
          title=data["name"],
          color=defaults.color
        )

        fields = {
          "Gender": [data["gender"].capitalize(), True],
          "Birth year": [data["birth_year"], True],
          "Height": [f"{data['height']} cm", True],
          "Mass": [f"{data['mass']} kg", True],
          "Skin color": [data["skin_color"].capitalize(), True],
          "Hair color": [data["hair_color"].capitalize(), True],
          "Eye color": [data["eye_color"].capitalize(), True],
          "Homeworld": [self.getDataByURL(data["homeworld"])["name"], False],
          "Movies": ["\n".join(self.getMovieList(data)), False],
        }

        for name, (val, inline) in fields.items():
          personEmbed.add_field(
            name=name,
            value=val,
            inline=inline
          )

        await ctx.send(embed=personEmbed)

      else:
        await ctx.send("Person not found")

    else:
      await Paginator(pages=self.getPaginator(objectType)).start(ctx)

  @cog_ext.cog_subcommand(
    base="starwars",
    name="planet",
    description="Get a planet from Star Wars",
    options = [
      create_option(
        name="planet",
        description="Planet in Star Wars",
        option_type=3,
        required=False
      )
    ],
    guild_ids=[694470208315719750]
  )
  async def starwars_planet(self, ctx: SlashContext, planet=None):
    await ctx.defer()

    objectType = "planets"

    if planet:
      data = self.getDataByName(objectType, planet)

      if data:
        planetEmbed = discord.Embed(
          title=data["name"],
          color=defaults.color
        )

        fields = {
          "Rotation period": [f"{data['rotation_period']} hours", True],
          "Orbital period": [f"{data['orbital_period']} days", True],
          "Diameter": [f"{data['diameter']} km", True],
          "Climate": [data["climate"].capitalize(), True],
          "Gravity": [data["gravity"], True],
          "Terrain": [data["terrain"].capitalize(), True],
          "Population": [data["population"], True],
          "Movies": ["\n".join(self.getMovieList(data)) if self.getMovieList(data) else "None", False],
        }

        for name, (val, inline) in fields.items():
          planetEmbed.add_field(
            name=name,
            value=val,
            inline=inline
          )

        await ctx.send(embed=planetEmbed)

      else:
        await ctx.send("Planet not found")

    else:
      await Paginator(pages=self.getPaginator(objectType)).start(ctx)

  @cog_ext.cog_subcommand(
    base="starwars",
    name="starship",
    description="Get a starship from Star Wars",
    options = [
      create_option(
        name="starship",
        description="Starship in Star Wars",
        option_type=3,
        required=False
      )
    ],
    guild_ids=[694470208315719750]
  )
  async def starwars_starship(self, ctx: SlashContext, starship=None):
    await ctx.defer()

    objectType = "starships"

    if starship:
      data = self.getDataByName(objectType, starship)

      if data:
        starshipEmbed = discord.Embed(
          title=data["name"],
          color=defaults.color
        )

        fields = {
          "Model": [data["model"], True],
          "Manufacturer": [f"{data['manufacturer']}", True],
          "Price": [f"{data['cost_in_credits']} credits", True],
          "Length": [f"{data['length']} m", True],
          "Maximum atmospheric speed ": [f"{data['max_atmosphering_speed']} kph", True],
          "Crew amount": [f"{data['crew']} people", True],
          "Passenger amount": [f"{data['passengers']} people", True],
          "Hyperdrive rating": [data["hyperdrive_rating"], True],
          "Sublight speed": [f"{data['MGLT']} MGLT", True],
          "Pilots": ["\n".join(self.getPeopleList(data, "pilots")), True],
          "Movies": ["\n".join(self.getMovieList(data)), False],
        }

        for name, (val, inline) in fields.items():
          starshipEmbed.add_field(
            name=name,
            value=val,
            inline=inline
          )

        await ctx.send(embed=starshipEmbed)

      else:
        await ctx.send("Starship not found")

    else:
      await Paginator(pages=self.getPaginator(objectType)).start(ctx)

  @cog_ext.cog_subcommand(
    base="starwars",
    name="species",
    description="Get a species from Star Wars",
    options = [
      create_option(
        name="species",
        description="Starwars species",
        option_type=3,
        required=False
      )
    ],
    guild_ids=[694470208315719750]
  )
  async def starwars_species(self, ctx: SlashContext, species=None):
    await ctx.defer()

    objectType = "species"

    if species:
      data = self.getDataByName(objectType, species)

      if data:
        speciesEmbed = discord.Embed(
          title=data["name"],
          color=defaults.color
        )

        fields = {
          "Classification": [data["classification"].capitalize(), True],
          "Designation": [data["designation"].capitalize(), True],
          "Average height": [f"{data['average_height']} cm", True],
          "Average lifespan": [f"{data['average_lifespan']} years", True],
          "Homeworld ": [self.getDataByURL(data["homeworld"])["name"], True],
          "Language": [data["language"], True],
          "People": ["\n".join(self.getPeopleList(data, "people")), False],
          "Movies": ["\n".join(self.getMovieList(data)), False],
        }

        for name, (val, inline) in fields.items():
          speciesEmbed.add_field(
            name=name,
            value=val,
            inline=inline
          )

        await ctx.send(embed=speciesEmbed)

      else:
        await ctx.send("Species not found")

    else:
      await Paginator(pages=self.getPaginator(objectType)).start(ctx)

  @cog_ext.cog_subcommand(
    base="starwars",
    name="vehicle",
    description="Get a vehicle from Star Wars",
    options = [
      create_option(
        name="vehicle",
        description="Starwars vehicle",
        option_type=3,
        required=False
      )
    ],
    guild_ids=[694470208315719750]
  )
  async def starwars_vehicle(self, ctx: SlashContext, vehicle=None):
    await ctx.defer()

    objectType = "vehicles"

    if vehicle:
      data = self.getDataByName(objectType, vehicle)

      if data:
        vehicleEmbed = discord.Embed(
          title=data["name"],
          color=defaults.color
        )

        fields = {
          "Model": [data["model"], True],
          "Manufacturer": [data["manufacturer"], True],
          "Price": [f"{data['cost_in_credits']} credits", True],
          "Length": [f"{data['length']} m", True],
          "Maximum atmospheric speed ": [f"{data['max_atmosphering_speed']} kph", True],
          "Crew amount": [f"{data['crew']} people", True],
          "Passenger amount": [f"{data['passengers']} people", True],
          "Pilots": ["\n".join(self.getPeopleList(data, "pilots")), True],
          "Movies": ["\n".join(self.getMovieList(data)), False],
        }

        for name, (val, inline) in fields.items():
          vehicleEmbed.add_field(
            name=name,
            value=val,
            inline=inline
          )

        await ctx.send(embed=vehicleEmbed)

      else:
        await ctx.send("Vehicle not found")

    else:
      await Paginator(pages=self.getPaginator(objectType)).start(ctx)

def setup(bot):
  bot.add_cog(StarWars(bot))