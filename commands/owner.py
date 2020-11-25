import discord
from discord.ext import commands
from core.EcoCore import *
import sqlite3

conn = sqlite3.connect('data\\bot.db')

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
            await ctx.send("Please mention someone to wipe.")
            return
        reason = ' '.join(reason)
        if reason == '':
            reason = 'None'
        try:
            file2.delete(member.id)
        except ValueError:
            await ctx.send(f"Couldn't wipe `{member.name}`: User is not in the database.")
        await ctx.send(f"Successfully wiped `{member.name}` from the database: `{reason}`")
        await member.send(f"You were wiped from my database by `{ctx.author.name}` with reason `{reason}`")
        print(f'{ctx.author.name} wiped {member.name} from the database: {reason}')

    @commands.command(aliases=['blist'])
    async def blacklist(self, ctx, member: discord.Member=None, *reason):
        """ Blacklists someone from the economy. """
        if member is None:
            await ctx.send("Please mention someone to blacklist.")
            return
        reason = ' '.join(reason)
        if reason == '':
            reason = 'None'
        cursor = conn.execute("SELECT * from BLACKLIST")
        try:
            for row in cursor:
                if row[0] == member.id:
                    raise error.UNABLE
        except error.UNABLE:
            await ctx.send(f"`{member}` is already blacklisted. Reason: `{reason}`.")
            return
        else:
            conn.execute(f"INSERT INTO BLACKLIST (USER,REASON) \
                    VALUES ({member.id}, '{reason}')")
            conn.commit()
            await ctx.send(f"Successfully blacklisted `{member}`. Reason: `{reason}`")
            await member.send(f"You were blacklisted from using my economy by `{ctx.author}`. Reason: `{reason}`")
            print(f'{ctx.author} blacklisted {member}. Reason: {reason}')

    @commands.command(aliases=['unblist'])
    async def unblacklist(self, ctx, member: discord.Member=None):
        """ Unblacklists someone from the economy. """
        if member is None:
            await ctx.send("Please mention someone to unblacklist.")
            return
        try:
            conn.execute(f"DELETE from BLACKLIST where USER = {member.id};")
        except sqlite3.OperationalError as e:
            if str(e) == f'no such column: {member.id}':
                raise ValueError
            else:
                raise e
        conn.commit()
        await ctx.send(f"Successfully unblacklisted `{member}`.")
        await member.send(f"You were removed from my blacklist by `{ctx.author}`. You should now be able to use my economy.")
        print(f'{ctx.author} unblacklisted {member}')

    @commands.command(aliases=['amoney'])
    async def addmoney(self, ctx, member: discord.Member=None, money: str=None, location: str='wallet'):
        """ Adds money to someone's balance. """
        if member is None:
            await ctx.send('Please specify which user to add money to.')
            return
        elif money is None:
            await ctx.send(f'Please specify the amount of money you would like to add to {member.name}')
            return
        try:
            money = int(money)
        except ValueError:
            await ctx.send(f'Please enter a number for the `money` argument.')
            return
        location = location.lower()
        if location == 'wallet':
            wallet.add(member.id, money)
        elif location == 'bank':
            bank.add(member.id, money)
        await ctx.send(f"Added ${money} to {member}'s {location}.")

    @commands.command(aliases=['remmoney','remony','rmoney'])
    async def removemoney(self, ctx, member: discord.Member=None, money: str=None, location: str='wallet'):
        """ Removes money from someone's balance. """
        if member is None:
            await ctx.send('Please specify which user to add money to.')
            return
        elif money is None:
            await ctx.send(f'Please specify the amount of money you would like to add to {member.name}')
            return
        try:
            money = int(money)
        except ValueError:
            await ctx.send(f'Please enter a number for the `money` argument.')
            return
        location = location.lower()
        if location == 'wallet':
            wallet.remove(member.id, money)
        elif location == 'bank':
            bank.remove(member.id, money)
        await ctx.send(f"Removed ${money} from {member}'s {location}.")

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
            await ctx.send(embed=embed)
            print(f"Couldn't unload extension {cog}: {e}")
        else:
            embed = discord.Embed(title='Success', description=f'Successfully unloaded extension {cog}', color=0xff0000)
            await ctx.send(embed=embed)

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
            await ctx.send(embed=embed)
            print(f"Couldn't load extension {cog}: {e}")
        else:
            embed = discord.Embed(title='Success', description=f'Successfully loaded extension {cog}', color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def reload(self, ctx, *, cog: str):
        """Reload an extension.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.reload_extension(cog)
            print(f'Successfully reloaded extension {cog}.')
        except Exception as e:
            embed = discord.Embed(title='Error', description=str(e), color=0xff0000)
            await ctx.send(embed=embed)
            print(f"Couldn't reload extension {cog}: {e}")
        else:
            embed = discord.Embed(title='Success', description=f'Successfully reloaded extension {cog}', color=0xff0000)
            await ctx.send(embed=embed)

    @commands.command()
    async def stop(self, ctx):
        """ Shutdown the bot. """
        print('Bot shutting down...')
        try:
            self.bot.logout()
        except Exception as e:
            embed = discord.Embed(title='Error', description=str(e), color=0xff0000)
            await ctx.send(embed=embed)
            print(f"Couldn't stop the bot: {e}")

def setup(bot):
    bot.add_cog(Restricted(bot))