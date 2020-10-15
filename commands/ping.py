import discord
from discord.ext import commands


class PingCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send(f'Pong! **`{self.bot.latency}`**')

def setup(bot):
    bot.add_cog(PingCMD(bot))