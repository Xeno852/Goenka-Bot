import os
import asyncio
from dotenv import load_dotenv
from mutagen.mp3 import MP3
import discord
from discord.ext import commands
from utils.helpers import initialize_db
from meditation import Meditation

# Load environment variables
load_dotenv()
token = os.getenv('APITOKEN') # Make sure your token is stored in the .env file

# Initialize bot with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize database
initialize_db()

# Add Meditation cog
bot.add_cog(Meditation(bot))

# Event when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    

# Ping command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Start meditation command
@bot.command()
async def start_meditation(ctx, duration: int):
    # Paths to audio files
    intro_chanting_path = "data/audio/intro-chanting.mp3"
    outro_chanting_path = "data/audio/outro-chanting.mp3"
    # Load audio files
    intro_chant = discord.FFmpegPCMAudio(intro_chanting_path)
    outro_chant = discord.FFmpegPCMAudio(outro_chanting_path)
    
    # Get durations of the audio files
    intro_chant_duration = MP3(intro_chanting_path).info.length
    outro_chant_duration = MP3(outro_chanting_path).info.length
    
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention} You must be in a voice channel to start a meditation session.")
        return
    
    # Announce meditation session
    await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")
    await ctx.send(f"Duration: {duration} minutes")
    
    # Connect to voice channel
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    members = voice_channel.members
    print("Loading users in current voice channels...")

    start_member_list = [member.id for member in members]
    
    
    
    # Play intro audio
    vc.play(intro_chant)
    
    # Wait for the meditation duration minus the intro audio duration
    await asyncio.sleep((duration * 60) - intro_chant_duration)
    
    # Send message indicating session is ending soon
    await ctx.send("Meditation session is coming to an end.")
    
    # Play outro audio
    vc.play(outro_chant)

    members = voice_channel.members
    print("Loading users in current voice channels...")

    end_member_list = [member.id for member in members]    
    
    #compare start_member_list and end_member_list and if the user is in both lists, add 1 to their streak in the database
    for member in start_member_list:
        if member in end_member_list:
            print("{} meditated the entire time!".format(member))
            #add 1 to their streak in the database
        else:
            # print("member is not in both lists")
            print("{} did not meditate the entire time!".format(member))

            #do nothing

    #Wait a little so it feels more natural before leaving

    
    await asyncio.sleep(15)
    
    # Disconnect from the voice channel
    await vc.disconnect()



# Start meditation command
@bot.command()
async def start_meditation_debug(ctx, duration: int):
    # Paths to audio files
    intro_chanting_path = "data/audio/intro-chanting.mp3"
    outro_chanting_path = "data/audio/outro-chanting.mp3"
    
    # Load audio files
    intro_chant = discord.FFmpegPCMAudio(intro_chanting_path)
    outro_chant = discord.FFmpegPCMAudio(outro_chanting_path)
    
    # Get durations of the audio files
    intro_chant_duration = MP3(intro_chanting_path).info.length
    outro_chant_duration = MP3(outro_chanting_path).info.length
    
    members = voice_channel.members
    # for member in members:
    #     await ctx.send(member.mention)


    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention} You must be in a voice channel to start a meditation session.")
        return
    
    # Announce meditation session
    await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")
    await ctx.send(f"Duration: {duration} minutes")
    
    # Connect to voice channel
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    
    # Play intro audio
    vc.play(intro_chant)
    
    # Wait for the meditation duration minus the intro audio duration
    await asyncio.sleep((duration * 60) - intro_chant_duration)
    
    # Send message indicating session is ending soon
    await ctx.send("Meditation session is coming to an end.")
    
    # Play outro audio
    vc.play(outro_chant)
    
    #Wait a little so it feels more natural before leaving
    await asyncio.sleep(15)

    # Disconnect from the voice channel
    await vc.disconnect()








# --------------------------------------------

# Start meditation command
@bot.command()
async def full_time_test(ctx):
    duration = 10
    # Paths to audio files
    intro_chanting_path = "data/audio/intro-chanting.mp3"
    outro_chanting_path = "data/audio/outro-chanting.mp3"
    # Load audio files
    intro_chant = discord.FFmpegPCMAudio(intro_chanting_path)
    outro_chant = discord.FFmpegPCMAudio(outro_chanting_path)
    
    # Get durations of the audio files
    intro_chant_duration = MP3(intro_chanting_path).info.length
    outro_chant_duration = MP3(outro_chanting_path).info.length
    
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention} You must be in a voice channel to start a meditation session.")
        return
    
    # Announce meditation session
    await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")
    await ctx.send(f"Duration: {duration} seconds")
    
    # Connect to voice channel
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    members = voice_channel.members
    print("Loading users in current voice channels...")

    start_member_list = [member.id for member in members]
    print("start_member_list: {}".format(start_member_list))

    # Send message indicating session is ending soon
    await asyncio.sleep(duration)
    await ctx.send("Meditation session is coming to an end.")
    


    members = voice_channel.members
    print("Loading users in current voice channels...")

    end_member_list = [member.id for member in members]    
    
    print("end_member_list: {}".format(end_member_list))
    #compare start_member_list and end_member_list and if the user is in both lists, add 1 to their streak in the database
    for member in start_member_list:
        if member in end_member_list:
            print("{} meditated the entire time!".format(member))
            #add 1 to their streak in the database
        else:
            # print("member is not in both lists")
            print("{} did not meditate the entire time!".format(member))

            #do nothing

    #Wait a little so it feels more natural before leaving

    
    await asyncio.sleep(15)
    
    # Disconnect from the voice channel
    await vc.disconnect()








# ----------------------------------------------




# Start meditation command
@bot.command()
async def full_time_test(ctx):
    duration = 10
    # Paths to audio files
    intro_chanting_path = "data/audio/intro-chanting.mp3"
    outro_chanting_path = "data/audio/outro-chanting.mp3"
    # Load audio files
    intro_chant = discord.FFmpegPCMAudio(intro_chanting_path)
    outro_chant = discord.FFmpegPCMAudio(outro_chanting_path)
    
    # Get durations of the audio files
    intro_chant_duration = MP3(intro_chanting_path).info.length
    outro_chant_duration = MP3(outro_chanting_path).info.length
    
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention} You must be in a voice channel to start a meditation session.")
        return
    
    # Announce meditation session
    await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")
    await ctx.send(f"Duration: {duration} seconds")
    
    # Connect to voice channel
    voice_channel = ctx.author.voice.channel
    vc = await voice_channel.connect()
    members = voice_channel.members
    print("Loading users in current voice channels...")

    start_member_list = [member.id for member in members]
    print("start_member_list: {}".format(start_member_list))

    # Send message indicating session is ending soon
    await asyncio.sleep(duration)
    await ctx.send("Meditation session is coming to an end.")
    


    members = voice_channel.members
    print("Loading users in current voice channels...")

    end_member_list = [member.id for member in members]    
    
    print("end_member_list: {}".format(end_member_list))
    #compare start_member_list and end_member_list and if the user is in both lists, add 1 to their streak in the database
    for member in start_member_list:
        if member in end_member_list:
            print("{} meditated the entire time!".format(member))
            #add 1 to their streak in the database
            #add duration to their total time in the database
            #add timestamp and duration to their session history in the database with the unique session id
            #update average time in the database

            # has extra database stuff so that it can be used for cool stats stuff later.. maybe like graphs

        else:
            # print("member is not in both lists")
            print("{} did not meditate the entire time!".format(member))

            #do nothing

    #Wait a little so it feels more natural before leaving

    
    await asyncio.sleep(15)
    
    # Disconnect from the voice channel
    await vc.disconnect()








#####---------------------------------------------









@bot.command()
async def vc_mems(ctx):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send(f"{ctx.author.mention} You must be in a voice channel.")
        return

    # Get the voice channel
    voice_channel = ctx.author.voice.channel

    # Retrieve the members in the voice channel
    members = voice_channel.members

    # Mention each member in the voice channel
    for member in members:
        await ctx.send(member.mention)

    member_list = [member.id for member in members]
    await ctx.send(members)
    await ctx.send(member_list)

# Run the bot with the token
bot.run(token)