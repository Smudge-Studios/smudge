from core.UtilCore import *
import discord
from discord.ext import commands
import sqlite3

utils = Utils()

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild
        cursor = conn.execute("SELECT * from COUNTING")
        for row in cursor:
            if row[0] == guild.id:
                if message.channel.id == row[1]:
                    try:
                        msg = int(message.content)
                    except ValueError:
                        try:
                            await message.delete()
                        except discord.Forbidden:
                            return
                        return
                    if msg == row[2]+1:
                        utils.count(guild.id, msg)
                    else:
                        try:
                            await message.delete()
                        except discord.Forbidden:
                            return

def setup(bot):
    bot.add_cog(Counting(bot))