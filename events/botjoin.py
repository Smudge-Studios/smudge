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
            me = guild.get_member(self.bot.user.id)
            perms = channel.permissions_for(me)
            if perms.send_messages:
                await channel.send("Hello, thanks for adding me!\nMy default prefix is `>`, please run `>help` to get started!")
                break 
            
def setup(bot):
    bot.add_cog(BotJoin(bot))