import discord
from discord.ext import commands
from core.UtilCore import Utils

utils = Utils()

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
        utils.setprefix(ctx, prefix)
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
            utils.setcountingchannel(ctx, 'remove')
            await ctx.send("Successfully removed counting channel from the database.")
            return
        else:
            try:
                channel = ctx.guild.get_channel(int(channel.replace('<#','').replace('>','')))
            except ValueError:
                await ctx.send("Couldn't find that channel.")
                return
            if channel == None:
                await ctx.send("Couldn't find that channel.")
                return
        utils.setcountingchannel(ctx, channel)
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
            utils.setsuggestionchannel(ctx, 'remove')
            await ctx.send("Successfully removed suggestion channel from the database.")
            return
        else:
            try:
                channel = ctx.guild.get_channel(int(channel.replace('<#','').replace('>','')))
            except ValueError:
                await ctx.send("Couldn't find that channel.")
                return
            if channel == None:
                await ctx.send("Couldn't find that channel.")
                return
        utils.setsuggestionchannel(ctx, channel)
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
            utils.setreportchannel(ctx, 'remove')
            await ctx.send("Successfully removed reports channel from the database.")
            return
        else:
            try:
                channel = ctx.guild.get_channel(int(channel.replace('<#','').replace('>','')))
            except ValueError:
                await ctx.send("Couldn't find that channel.")
                return
            if channel == None:
                await ctx.send("Couldn't find that channel.")
                return
        utils.setreportchannel(ctx, channel)
        await ctx.send(f'Successfully set reports channel to <#{channel.id}>.')

def setup(bot):
    bot.add_cog(Server(bot))