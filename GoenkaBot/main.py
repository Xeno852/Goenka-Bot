import discord
from discord.ext import commands
import json
import os
from utils.helpers import initialize_db

# Load settings
with open("config/settings.json", "r") as file:
    settings = json.load(file)

# Initialize bot
bot = commands.Bot(command_prefix=settings["prefix"])

# Initialize database
initialize_db()

# Load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Run bot
bot.run(settings["token"])
