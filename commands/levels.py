import discord
from discord.ext import commands
from core.LevelCore import Levels
import random
from core.UtilCore import Utils

levels = Levels()
utils = Utils()

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Cog check. Checks if blacklisted user invoked cog."""
        if not await utils.levelson(ctx.guild.id):
            await ctx.reply("Sorry, the level system in this guild is disabled.")
            raise commands.DisabledCommand
        return True

    @commands.command()
    async def rank(self, ctx, member: discord.Member=None):
        discord.InvalidData
        color=random.randint(1, 16777215)
        if member is None:
            member = ctx.author
        if member.bot:
            await ctx.reply("Cannot check the rank of a bot.")
            return
        level, xp, progressbar, msgs = await levels.fetchrank(member.id, ctx.guild.id)
        embed = discord.Embed(title=f"{member.name}'s Rank", description=f"""Level: {level}
Messages: {msgs}
Experience: {xp}
{progressbar}""", color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=embed)

    @rank.error
    async def eh99999(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command()
    async def levels(self, ctx):
        """ Check the guild's Leveling leaderboard. """
        color=random.randint(1, 16777215)
        lvls, lvldict = await levels.leaders(ctx.guild.id)
        lvls.sort(reverse=True)
        lvls = lvls[:10]
        e = ''
        en = 0
        for i in lvls:
            id1 = lvldict[i]
            if isinstance(id1, list):
                for a in id1:
                    en += 1
                    e += f"{en}. <@{a}>: Level {i}\n"
                del lvldict[i]
            else:
                en += 1
                e += f"{en}. <@{id1}>: Level {i}\n"
                del lvldict[i]
        embed = discord.Embed(title=f"{ctx.guild.name}'s Leaderboard", description=e, color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def addxp(self, ctx, member: discord.Member=None, amount: str=None):
        """ Add XP to a member. """
        if member is None:
            await ctx.reply("Please provide a member.")
            return
        if member.bot:
            await ctx.reply("You cannot add XP to a bot.")
            return
        if amount is None:
            await ctx.reply("Please provide the amount of XP.")
            return
        if '-' in amount:
            await ctx.reply("You cannot provide a negative number as an amount.")
            return
        try:
            amnt = int(amount)
        except ValueError:
            await ctx.reply("Invalid amount.")
            return
        lvls = await levels.addexp(member, ctx.guild.id, amnt)
        if lvls != -1:
            ranks = await levels.getranks(ctx.guild.id)
            for r in ranks:
                if r <= lvls:
                    role = ctx.guild.get_role(ranks[r])
                    try:
                        await member.add_roles(role)
                    except:
                        pass
            await ctx.reply(f"Successfully added {amnt} XP to {member}. They are now level {lvls}.")
        else:
            await ctx.reply(f"Successfully added {amnt} XP to {member}. Their level has not changed.")

    @addxp.error
    async def errrrrrrrrrrrr(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid member.")

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def removexp(self, ctx, member: discord.Member=None, amount: str=None):
        """ Remove XP from a member. """ 
        if member is None:
            await ctx.reply("Please provide a member.")
            return
        if member.bot:
            await ctx.reply("You cannot remove XP from a bot.")
            return
        if amount is None:
            await ctx.reply("Please provide the amount of XP.")
            return
        if '-' in amount:
            await ctx.reply("You cannot provide a negative number as an amount.")
            return
        try:
            amnt = int(amount)
        except ValueError:
            await ctx.reply("Invalid amount.")
            return
        try:
            lvls = await levels.remexp(member, ctx.guild.id, amnt)
        except ValueError as e:
            await ctx.reply(str(e))
            return
        if lvls != -1:
            ranks = await levels.getranks(ctx.guild.id)
            for r in ranks:
                if r > lvls:
                    role = ctx.guild.get_role(ranks[r])
                    try:
                        await member.remove_roles(role)
                    except:
                        pass
            await ctx.reply(f"Successfully removed {amnt} XP from {member}. They are now level {lvls}.")
        else:
            await ctx.reply(f"Successfully removed {amnt} XP from {member}. Their level has not changed.")

    @removexp.error
    async def errrrrrrrrrarrr(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid member.")

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def addrank(self, ctx, level: str=None, role: discord.Role=None):
        """ Add or change a reward for passing a certain level. """
        if level is None:
            await ctx.reply("Please provide a level.")
            return
        if role is None:
            await ctx.reply("Please provide a role.")
            return
        try:
            level = int(level)
        except ValueError:
            await ctx.reply("Invalid level. Please provide an integer.")
            return
        response = await levels.addrank(ctx.guild.id, role.id, level)
        if response == 'added':
            await ctx.reply(f"Successfully added the role {role.name} as a reward for level {str(level)}.")
            return
        if response == 'updated':
            await ctx.reply(f"Successfully set the reward for level {level} to the role {role.name}.")
            return

    @removexp.error
    async def ehgobrrrr(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid role.")

    @commands.command(aliases=['delrank'])
    @commands.has_guild_permissions(manage_guild=True)
    async def deleterank(self, ctx, level: str=None):
        """ Remove a reward for passing a certain level. """
        if level is None:
            await ctx.reply("Please provide a level.")
            return
        try:
            level = int(level)
        except ValueError:
            await ctx.reply("Invalid level. Please provide an integer.")
            return
        try:
            await levels.deleterank(ctx.guild.id, level)
            await ctx.reply(f"Successfully removed the the reward for level {level}.")
            return
        except ValueError:
            await ctx.reply(f"There are no rewards set for level {level}.")
            return

def setup(bot):
    bot.add_cog(Leveling(bot))