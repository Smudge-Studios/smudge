import discord
from discord.ext import commands


class PingCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! **`{round(bot.latency * 1000)}`ms.**")

def setup(bot):
    bot.add_cog(PingCMD(bot))