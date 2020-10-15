import discord
from discord.ext import commands
import asyncio
        
class OnReady(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(' Successfully logged in as ' + self.bot.user.name + ' | ' + str(self.bot.user.id) + '.')
        print('Bot Started')
        while True:
            try:
                member_count = len([m for m in ctx.guild.members if not m.bot]) # doesn't include bots
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {member_count} members | s!help"))
                await asyncio.sleep(delay)
            except:
                await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="for commands | s!help"))
                await asyncio.sleep(delay)

def setup(bot):
    bot.add_cog(OnReady(bot))