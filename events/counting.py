import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('data\\config.db')

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
                            await ctx.send()
                            return
                        return
                    if msg == row[2]+1:
                        conn.execute(f"UPDATE COUNTING set NUMBER = {msg} where GUILD = {guild.id}")
                        return
                    else:
                        try:
                            await message.delete()
                        except discord.Forbidden:
                            return

def setup(bot):
    bot.add_cog(Counting(bot))