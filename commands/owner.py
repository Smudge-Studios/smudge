import discord
from discord.ext import commands
from core.EcoCore import *
import aiosqlite
from core.UtilCore import Utils
from core.ModCore import Mod

modcore = Mod()
utils = Utils()

class Restricted(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Cog check. Checks if owner invoked cog."""
        if await self.bot.is_owner(ctx.author):
            return True
        raise commands.NotOwner()

    @commands.command(aliases=['statwipe','statswipe','balwipe','wipebal','wipestats'])
    async def wipe(self, ctx, member: discord.Member=None, *reason):
        """ Wipes somebody's balance. """
        if member is None:
            await ctx.reply("Please mention someone to wipe.")
            return
        reason = ' '.join(reason)
        if reason == '':
            reason = 'None'
        try:
            await data.delete(member.id)
        except ValueError:
            await ctx.reply(f"Couldn't wipe `{member.name}`: User is not in the database.")
        await ctx.reply(f"Successfully wiped `{member.name}` from the database: `{reason}`")
        await member.reply(f"You were wiped from my database by `{ctx.author.name}` with reason `{reason}`")
        print(f'{ctx.author.name} wiped {member.name} from the database: {reason}')

    @wipe.error
    async def eh699(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command(aliases=['blist'])
    async def blacklist(self, ctx, member: discord.Member=None, *reason):
        """ Blacklists someone from the economy. """
        if member is None:
            await ctx.reply("Please mention someone to blacklist.")
            return
        reason = ' '.join(reason)
        if reason == '':
            reason = 'None'
        async with aiosqlite.connect('data\\bot.db') as conn:
            async with conn.execute("SELECT * from BLACKLIST") as cursor:
                async for row in cursor:
                    if row[0] == member.id:
                        await ctx.reply(f"`{member}` is already blacklisted. Reason: `{reason}`.")
                        return
            await conn.execute(f"INSERT INTO BLACKLIST (USER,REASON) \
                    VALUES ({member.id}, '{reason}')")
            await conn.commit()
        await ctx.reply(f"Successfully blacklisted `{member}`. Reason: `{reason}`")
        await member.reply(f"You were blacklisted from using my economy by `{ctx.author}`. Reason: `{reason}`")
        print(f'{ctx.author} blacklisted {member}. Reason: {reason}')

    @blacklist.error
    async def eh69(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command(aliases=['unblist'])
    async def unblacklist(self, ctx, member: discord.Member=None):
        """ Unblacklists someone from the economy. """
        if member is None:
            await ctx.reply("Please mention someone to unblacklist.")
            return
        s = False
        async with aiosqlite.connect('data\\bot.db') as conn:
            async with conn.execute("SELECT * from BLACKLIST") as cursor:
                async for row in cursor:
                    if row[0] == member.id:
                        await conn.execute(f"DELETE from BLACKLIST where USER = {member.id};")
                        await conn.commit()
                        s = True
        if s:
            await ctx.reply(f"Successfully unblacklisted `{member}`.")
            await member.reply(f"You were removed from my blacklist by `{ctx.author}`. You should now be able to use my economy.")
            print(f'{ctx.author} unblacklisted {member}')
        else:
            await ctx.reply(f"`{member}` is not blacklisted.")

    @unblacklist.error
    async def eh691(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command(aliases=['amoney'])
    async def addmoney(self, ctx, member: discord.Member=None, money: str=None, location: str='wallet'):
        """ Adds money to someone's balance. """
        if member is None:
            await ctx.reply('Please specify which user to add money to.')
            return
        elif money is None:
            await ctx.reply(f'Please specify the amount of money you would like to add to {member.name}')
            return
        try:
            money = int(money)
        except ValueError:
            await ctx.reply(f'Please enter a number for the `money` argument.')
            return
        location = location.lower()
        if location == 'wallet':
            await wallet.add(member.id, money)
        elif location == 'bank':
            await bank.add(member.id, money)
        await ctx.reply(f"Added ${money} to {member}'s {location}.")

    @addmoney.error
    async def eh692(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command(aliases=['remmoney','remony','rmoney'])
    async def removemoney(self, ctx, member: discord.Member=None, money: str=None, location: str='wallet'):
        """ Removes money from someone's balance. """
        if member is None:
            await ctx.reply('Please specify which user to add money to.')
            return
        elif money is None:
            await ctx.reply(f'Please specify the amount of money you would like to add to {member.name}')
            return
        try:
            money = int(money)
        except ValueError:
            await ctx.reply(f'Please enter a number for the `money` argument.')
            return
        location = location.lower()
        if location == 'wallet':
            await wallet.remove(member.id, money)
        elif location == 'bank':
            await bank.remove(member.id, money)
        await ctx.reply(f"Removed ${money} from {member}'s {location}.")

    @removemoney.error
    async def eh693(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command()
    async def unload(self, ctx, *, cog: str):
        """Unload an extension.
        Remember to use dot path. e.g: cogs.owner"""
        print(f'{ctx.author} ({ctx.author.id}) is attempting to unload extension {cog}...')
        try:
            self.bot.unload_extension(cog)
            print(f'Successfully unloaded extension {cog}.')
        except Exception as e:
            embed = discord.Embed(title='Error', description=str(e), color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            print(f"Couldn't unload extension {cog}: {e}")
        else:
            embed = discord.Embed(title='Success', description=f'Successfully unloaded extension {cog}', color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)

    @commands.command()
    async def load(self, ctx, *, cog: str):
        """Load an extension.
        Remember to use dot path. e.g: cogs.owner"""
        print(f'{ctx.author} ({ctx.author.id}) is attempting to load extension {cog}...')
        try:
            self.bot.load_extension(cog)
            print(f'Successfully loaded extension {cog}.')
        except Exception as e:
            embed = discord.Embed(title='Error', description=str(e), color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            print(f"Couldn't load extension {cog}: {e}")
        else:
            embed = discord.Embed(title='Success', description=f'Successfully loaded extension {cog}', color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)

    @commands.command()
    async def reload(self, ctx, *, cog: str):
        """Reload an extension.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.reload_extension(cog)
            print(f'Successfully reloaded extension {cog}.')
        except Exception as e:
            embed = discord.Embed(title='Error', description=str(e), color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            print(f"Couldn't reload extension {cog}: {e}")
        else:
            embed = discord.Embed(title='Success', description=f'Successfully reloaded extension {cog}', color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)

    @commands.command()
    async def stop(self, ctx):
        """ Shutdown the bot. """
        print('Bot shutting down...')
        try:
            self.bot.logout()
        except Exception as e:
            embed = discord.Embed(title='Error', description=str(e), color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            print(f"Couldn't stop the bot: {e}")

    @commands.command()
    async def forceprefix(self, ctx, prefix):
        """ Forces the guild prefix to be something else. """
        if prefix is None:
            prefix = '>'
        elif prefix == '':
            await ctx.reply("Invalid argument. Please omit any quotes in the command.")
            return
        await utils.setprefix(ctx, prefix)
        await ctx.reply(f'Successfully changed the server prefix to `{prefix}`')

def setup(bot):
    bot.add_cog(Restricted(bot))