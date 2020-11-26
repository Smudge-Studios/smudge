import discord
from discord.ext import commands
from core.UtilCore import Utils

utils = Utils()

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['config'])
    @commands.has_guild_permissions(manage_guild=True)
    async def configuration(self, ctx):
        """ Manage server configuration. """
        if ctx.invoked_subcommand is None:
            config = utils.get_config(ctx)
            if config['mistbin']:
                mistbin = '<:greenTick:781603346640535622>'
            else:
                mistbin = '<:redTick:781603346510643230>'
            if config['token']:
                token = '<:greenTick:781603346640535622>'
            else:
                token = '<:redTick:781603346510643230>'
            if config['counting'] is None:
                counting = '<:redTick:781603346510643230>'
            else:
                counting = f"<#{config['counting']}>"
            if config['suggestions'] is None:
                suggestions = '<:redTick:781603346510643230>'
            else:
                suggestions = f"<#{config['suggestions']}>"
            if config['reports'] is None:
                reports = '<:redTick:781603346510643230>'
            else:
                reports = f"<#{config['reports']}>"
            embed = discord.Embed(title="Configuration", description=f"""Prefix: `{config['prefix']}`
Counting Channel: {counting}
Suggestion Channel: {suggestions}
Reports Channel: {reports}
Upload TXT files to [mystbin](https://mystb.in): {mistbin}
Token Detector: {token}""")
            await ctx.send(embed=embed)
    
    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def suggestions(self, ctx, channel: str=None):
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

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def reports(self, ctx, channel: str=None):
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

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def counting(self, ctx, channel: str=None):
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

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str=None):
        """ Updates the server's prefix. """
        if prefix is None:
            prefix = '>'
        elif prefix == '':
            await ctx.send("Invalid argument. Please omit any quotes in the command.")
            return
        utils.setprefix(ctx, prefix)
        await ctx.send(f'Successfully changed the server prefix to `{prefix}`')

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def mystbin(self, ctx, setting: str=None):
        if setting is None:
            await ctx.send("Please provide a setting, either 'on' or 'off'.")
            return
        if setting.lower() == 'on':
            utils.mistbin(ctx, True)
        elif setting.lower() == 'off':
            utils.mistbin(ctx, False)
        else:
            await ctx.send("Invalid setting. Please provide either 'on' or 'off'.")
            return
        await ctx.send(f"Successfully toggled MystBin {setting.lower()}.")

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def token(self, ctx, setting: str=None):
        if setting is None:
            await ctx.send("Please provide a setting, either 'on' or 'off'.")
            return
        if setting.lower() == 'on':
            utils.tokenalerter(ctx, True)
        elif setting.lower() == 'off':
            utils.tokenalerter(ctx, False)
        else:
            await ctx.send("Invalid setting. Please provide either 'on' or 'off'.")
            return
        await ctx.send(f"Successfully toggled Token Detector {setting.lower()}.")

def setup(bot):
    bot.add_cog(Server(bot))