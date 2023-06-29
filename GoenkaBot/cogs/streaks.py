import discord
from discord.ext import commands
import sqlite3

class Streaks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def check_streaks(self, ctx):
        connection = sqlite3.connect("data/database.sqlite")
        cursor = connection.cursor()
        
        # Query streaks from the database
        cursor.execute("SELECT * FROM streaks")
        streaks = cursor.fetchall()
        
        # Create and send a message with streaks
        message = "User Streaks:\n"
        for user_id, streak_count in streaks:
            user = await self.bot.fetch_user(user_id)
            message += f"{user.name}: {streak_count}\n"
        
        await ctx.send(message)

        connection.close()

def setup(bot):
    bot.add_cog(Streaks(bot))
