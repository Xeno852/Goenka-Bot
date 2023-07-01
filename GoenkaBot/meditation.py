import discord
from discord.ext import commands
import asyncio
import sqlite3

class Meditation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Meditation cog initialized.")
    
    @commands.command()
    async def start_meditation(self, ctx, duration: int):
        # await ctx.send("This is a command from the cog."
    # async def start_meditation(self, ctx):
        print("Command start_meditation triggered")
        # Check if the user is in a voice channel
        if ctx.author.voice is None:
            await ctx.send("You must be in a voice channel to start a meditation session.")
            return

        # Announce meditation session
        await ctx.send(f"{ctx.author.mention} has started a meditation session! Join the voice channel to participate!")

        # Join voice channel
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()

        # Play intro audio
        vc.play(discord.FFmpegPCMAudio("data/audio/intro-chanting.mp3"))

        # Wait for duration
        await asyncio.sleep(duration)

        # Send message indicating session is ending soon
        await ctx.send("Meditation session is coming to an end.")

        # Play outro audio
        vc.play(discord.FFmpegPCMAudio("data/audio/outro-chanting.mp3"))

        # Wait for outro duration then leave
        outro_duration = 173  # You can adjust this based on the length of your outro audio
        await asyncio.sleep(outro_duration)
        await vc.disconnect()
        
        # TODO: Update streaks here

def setup(bot):
    print("Meditation cog loaded.")
    bot.add_cog(Meditation(bot))