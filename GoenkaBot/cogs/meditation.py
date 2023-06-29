import discord
from discord.ext import commands
import asyncio
import sqlite3

class Meditation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def start_meditation(self, ctx, duration: int):
        # Announce meditation session
        await ctx.send(f"{ctx.author} has started a meditation session! Join the voice channel to participate!")

        # Join voice channel
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()

        # Play intro audio
        vc.play(discord.FFmpegPCMAudio("data/audio/intro-chanting.mp3"))

        # Wait for duration
        await asyncio.sleep(duration)

        # Play outro audio
        vc.play(discord.FFmpegPCMAudio("data/audio/outro-chanting.mp3"))

        # Wait for outro duration then leavei
        outro_duration = 173 #based on the file
        await asyncio.sleep(outro_duration)  # Assuming outro is 10 seconds
        await vc.disconnect()
        
        # TODO: Update streaks here

def setup(bot):
    bot.add_cog(Meditation(bot))
