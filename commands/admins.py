import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('data\\config.db')

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix: str=None):
        """ Updates the server's prefix. """
        if prefix is None:
            prefix = '>'
        elif prefix == '':
            await ctx.send("Invalid argument. Please omit any quotes in the command.")
            return
        guild = ctx.guild.id
        conn.execute(f"UPDATE CONFIG set PREFIX = {prefix} where GUILD = {guild}")
        conn.commit()
        await ctx.send(f'Successfully changed the server prefix to `{prefix}`')

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def count(self, ctx, channel: str=None):
        """ Define a counting channel, or have the bot create one. """
        guild = ctx.guild
        if channel is None:
            await ctx.send('Please provide a channel.')
            return
        elif channel.lower() == 'create':
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    guild.me: discord.PermissionOverwrite(read_messages=True, manage_messages=True)
                }
                channel = await guild.create_text_channel('counting', topic="A counting channel.", overwrites=overwrites, reason=f"Counting channel requested by {ctx.author.name}.")
            except discord.Forbidden:
                await ctx.send("I do not have the required permissions to create a channel.")
                return
            await ctx.send(f"Text channel created. (<#{channel.id}>)")
        elif channel.lower() == 'remove':
            conn.execute(f"UPDATE COUNTING set CHANNEL = Null where GUILD = {guild.id}")
            await ctx.send("Successfully removed counting channel from the database.")
        else:
            try:
                channel = guild.get_channel(int(channel.replace('<@','').replace('>','')))
            except ValueError:
                await ctx.send('Invalid channel.')
                return
            if channel == None:
                await ctx.send("Couldn't find that channel.")
                return
        cursor = conn.execute("SELECT * from COUNTING")
        try:
            for row in cursor:
                if row[0] == ctx.guild.id:
                    conn.execute(f"UPDATE COUNTING set CHANNEL = {channel.id} where GUILD = {guild.id}")
                    break
            raise ValueError
        except ValueError:
            conn.execute(f"INSERT INTO COUNTING (GUILD,CHANNEL,NUMBER) \
                VALUES ({ctx.guild.id}, {channel.id}, 0)")
        conn.commit()
        await ctx.send(f'Successfully set counting channel to <#{channel.id}>.')

    @commands.command(aliases=['suggestchannel','sc'])
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def suggestionchannel(self, ctx, channel: str=None):
        """ Define a suggestion channel, or have the bot create one. """
        guild = ctx.guild
        if channel is None:
            await ctx.send('Please provide a channel.')
            return
        elif channel.lower() == 'create':
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                channel = await guild.create_text_channel('suggestions', topic="A suggestion channel.", overwrites=overwrites, reason=f"Suggestion channel requested by {ctx.author.name}.")
            except discord.Forbidden:
                await ctx.send("I do not have the required permissions to create a channel.")
                return
            await ctx.send(f"Text channel created. (<#{channel.id}>)")
        elif channel.lower() == 'remove':
            conn.execute(f"UPDATE CONFIG set SUGGESTIONS = Null where GUILD = {guild.id}")
            await ctx.send("Successfully removed counting channel from the database.")
        else:
            try:
                channel = guild.get_channel(int(channel.replace('<@','').replace('>','')))
            except ValueError:
                await ctx.send('Invalid channel.')
                return
            if channel == None:
                await ctx.send("Couldn't find that channel.")
                return
        cursor = conn.execute("SELECT * from CONFIG")
        for row in cursor:
            if row[0] == ctx.guild.id:
                conn.execute(f"UPDATE CONFIG set SUGGESTIONS = {channel.id} where GUILD = {guild.id}")
                break
        conn.commit()
        await ctx.send(f'Successfully set suggestion channel to <#{channel.id}>.')

    @commands.command(aliases=['reportschannel','rc'])
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def reportchannel(self, ctx, channel: str=None):
        """ Define a reports channel, or have the bot create one. """
        guild = ctx.guild
        if channel is None:
            await ctx.send('Please provide a channel.')
            return
        elif channel.lower() == 'create':
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                channel = await guild.create_text_channel('reports', topic="A reports channel.", overwrites=overwrites, reason=f"Suggestion channel requested by {ctx.author.name}.")
            except discord.Forbidden:
                await ctx.send("I do not have the required permissions to create a channel.")
                return
            await ctx.send(f"Text channel created. (<#{channel.id}>)")
        elif channel.lower() == 'remove':
            conn.execute(f"UPDATE CONFIG set REPORTS = Null where GUILD = {guild.id}")
            await ctx.send("Successfully removed counting channel from the database.")
        else:
            try:
                channel = guild.get_channel(int(channel.replace('<@','').replace('>','')))
            except ValueError:
                await ctx.send('Invalid channel.')
                return
            if channel == None:
                await ctx.send("Couldn't find that channel.")
                return
        cursor = conn.execute("SELECT * from CONFIG")
        for row in cursor:
            if row[0] == ctx.guild.id:
                conn.execute(f"UPDATE CONFIG set REPORTS = {channel.id} where GUILD = {guild.id}")
                break
        conn.commit()
        await ctx.send(f'Successfully set suggestion channel to <#{channel.id}>.')

def setup(bot):
    bot.add_cog(Server(bot))