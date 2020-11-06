import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('data\\config.db')

class BotJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channels = guild.text_channels
        for channel in channels:
            try:
                await channel.send("Hello, thanks for adding me!\nMy default prefix is `>`, please run `>help` to get started!")
                break 
            except:
                pass
            
def setup(bot):
    bot.add_cog(BotJoin(bot))