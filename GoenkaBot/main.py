# Initialize bot
import discord
from discord.ext import commands
import json
import os
import importlib
import asyncio
from utils.helpers import initialize_db
from mutagen.mp3 import MP3
# from "GoenkaBot\cogs\meditation.py" import Meditation
from meditation import Meditation
# Load settings
with open("config/settings.json", "r") as file:
    settings = json.load(file)
# load token from json
token = settings["token"]
# Initialize bot
intents = discord.Intents.default()
intents = discord.Intents.all()

intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize database
initialize_db()

print("Loading cogs...")
# for filename in os.listdir("./cogs"):
#     if filename.endswith(".py") and filename != "__init__.py":
#         print(f"Loading {filename}...")
#         cog_name = filename[:-3]  # Remove '.py' extension
#         module = importlib.import_module(f"cogs.{cog_name}")

#         # Find the class derived from commands.Cog
#         for attr_name in dir(module):
#             attr = getattr(module, attr_name)
#             if isinstance(attr, type) and issubclass(attr, commands.Cog):
#                 cog_class = attr

#         bot.add_cog(cog_class(bot))



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.add_cog(Meditation(bot))

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")
    # await ctx.send(f"Hmm.. {discord.ext.commands.Meditation.get_commands()}")

@bot.command()
async def start_meditation(ctx, duration: int):
    intro_chanting_path = "data/audio/intro-chanting.mp3"
    outro_chanting_path = "data/audio/outro-chanting.mp3"

    intro_chant = discord.FFmpegPCMAudio(intro_chanting_path)
    outro_chant = discord.FFmpegPCMAudio(outro_chanting_path)

    intro_chant_file = MP3(intro_chanting_path)
    outro_chant_file = MP3(outro_chanting_path)

    intro_chant_duration = intro_chant_file.info.length
    outro_chant_duration = outro_chant_file.info.length

    await ctx.send("This is a command from the cog.")
    # durations of chants
    await ctx.send(f"Intro duration: {intro_chant_duration} minutes")
    await ctx.send(f"Outro duration: {outro_chant_duration} minutes")
# async def start_meditation(self, ctx):
    print("Command start_meditation triggered")
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("{} You must be in a voice channel to start a meditation session.".format(ctx.author.mention))
        return

    # Announce meditation session
    await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")
    await ctx.send(f"Duration: {duration} minutes")
    # Join voice channel
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()

    # Play intro audio
    # vc.play(discord.FFmpegPCMAudio("data/audio/intro-chanting.mp3"))
    vc.play(intro_chant)

    

    # Wait for duration
    await asyncio.sleep((duration*60) - intro_chant_duration) #change so duration is in minutes and subtract the intro time from the duration
    #make these not magic numbers..

    # Send message indicating session is ending soon
    await ctx.send("Meditation session is coming to an end.")


    # Play outro audio
    # vc.play(discord.FFmpegPCMAudio("data/audio/outro-chanting.mp3"))
    vc.play(outro_chant)

    # Wait for outro duration then leave
    # outro_duration = 173  # You can adjust this based on the length of your outro audio
    await asyncio.sleep(outro_chant_duration)
    await asyncio.sleep(15) # Sleep to feel more natural before leaving
    await vc.disconnect()

   # Run bot
bot.run(token) #   : Change this to your bot's token within the settings.json file
