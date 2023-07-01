import discord
from discord.ext import commands
import asyncio
import sqlite3

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    print("Announcements cog loaded.")
    bot.add_cog(Announcements(bot))