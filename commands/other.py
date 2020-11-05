import discord
from discord.ext import commands
from core.UtilCore import *
from core.Exceptions import *

utils = Utils()

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *, command: str=None):
        """ Displays a list of commands, or help on a specific command. """
        cogs = ['Util','Fun','Economy','Moderation','Server','Restricted']
        if command is None:
            embed = discord.Embed(title="Help")
            for i in cogs:
                cog = self.bot.get_cog(i)
                cmds = cog.get_commands()
                msg = ''
                for e in cmds:
                    msg = msg+str(e.name)
                    msg = msg+f" {e.usage} - "
                    msg = msg+str(e.brief)
                    msg = msg+"\n \n"
                    embed.add_field(name=cog.name, value=msg, inline=False)
        else:
            for i in cogs:
                if i.lower() == command.lower():
                    cog = self.bot.get_cog(i)
                    cmds = cog.get_commands()
                    msg = ''
                    for e in cmds:
                        msg = msg+str(e.name)
                        msg = msg+f" {e.usage} - "
                        msg = msg+str(e.brief)
                        msg = msg+"\n \n"
                        embed=discord.Embed(title=f"{cog.name}", description=msg)
                        await ctx.send(embed=embed)
                        return
            else:
                msg = ''
                cmd = self.bot.get_command(command.lower())
                if cmd is None:
                    await ctx.send("Command not found.")
                    return
                msg = msg+str(cmd.help)
                msg = msg+"\nUsage: "
                msg = msg+str(cmd.name)
                msg = msg+f" {cmd.usage}"
                aliases = ', '.join(cmd.aliases)
                msg = msg+"\nAliases: "
                msg = msg+aliases
                embed=discord.Embed(title=cmd.name, description=msg)
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        """ Information about the bot and the developer. """
        embed = discord.Embed(title="Info", description="""This bot was coded by `plun1331#5535` in [discord.py](discordpy.readthedocs.io) as a fun, open sourced project.
        It was first meant to be an economy bot, but I eventually made it into a multi-purpose bot with moderation, fun commands, an economy, and some server management tools.
        [Source code](https://github.com/Smudge-Studios/smudge)
        [Twitter](https://twitter.com/plun1331)
        [Github](https://github.com/plun1331)
        [YouTube](https://plun1331.github.io/youtube)""")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Other(bot))