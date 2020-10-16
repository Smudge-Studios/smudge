import discord
from discord.ext import commands


class CMDError(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Error", description="""Missing Required Argument.""", color=0xff0000)
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description="""Bad Argument.""", color=0xff0000)
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.MissingPermissions) or isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Error", description="""Insufficient permissions.""", color=0xff0000)
            await ctx.send(embed=embed)
            return
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Error", description="""That command is on a cooldown.""", color=0xff0000)
            await ctx.send(embed=embed)
            return
        else:
            embed = discord.Embed(title="Error", description="""An unknown error occurred. This error has been reported.
            `""" + str(error) + '`', color=0xff0000)
            await ctx.send(embed=embed)
            print("---------------")
            print("An unknown error occurred.")
            print("")
            print("=====(BEGIN ERROR OUTPUT)=====")
            raise (error)
            print("=====(END ERROR OUTPUT)=====")
            return

def setup(bot):
    bot.add_cog(CMDError(bot))