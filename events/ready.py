import discord
from discord.ext import commands

class OnReady(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(' Successfully logged in as ' + self.bot.user.name + ' | ' + str(self.bot.user.id) + '.')
        print('Bot started.')

def setup(bot):
    bot.add_cog(OnReady(bot))