import discord
from discord.ext import commands


class CMDError(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send('send help')

def setup(bot):
    bot.add_cog(CMDError(bot))