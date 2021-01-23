from core.AutoModSettings import AutoModSettingsManager
import discord
from discord.ext import commands
from core.UtilCore import Utils
from core.LevelCore import Levels
import random

yes = '<a:greenTick:784137919422005249>'
no = '<a:redTick:784137915269382185>'

utils = Utils()
levels = Levels()
automod = AutoModSettingsManager()

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['config'])
    @commands.has_guild_permissions(manage_guild=True)
    async def configuration(self, ctx):
        """ Manage server configuration. """
        if ctx.invoked_subcommand is None:
            config = await utils.get_config(ctx)
            if config['mistbin']:
                mistbin = yes
            else:
                mistbin = no
            if config['token']:
                token = yes
            else:
                token = no
            if config['counting'] is None:
                counting = no
            else:
                counting = f"<#{config['counting']}>"
            if config['suggestions'] is None:
                suggestions = no
            else:
                suggestions = f"<#{config['suggestions']}>"
            if config['reports'] is None:
                reports = no
            else:
                reports = f"<#{config['reports']}>"
            if config['levels']:
                levels = yes
            else:
                levels = no
            color=random.randint(1, 16777215)
            embed = discord.Embed(title="Configuration", description=f"""Prefix: `{config['prefix']}`
Counting Channel: {counting}
Suggestion Channel: {suggestions}
Reports Channel: {reports}
Upload TXT files to [mystbin](https://mystb.in): {mistbin}
Token Detector: {token}
Levels System: {levels}""", color=color)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
    
    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def suggestions(self, ctx, channel: str=None):
        """ Define a suggestion channel, or have the bot create one. """
        guild = ctx.guild
        if channel is None:
            await ctx.reply('Please provide a channel.')
            return
        elif channel.lower() == 'create':
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                channel = await guild.create_text_channel('suggestions', topic="A suggestion channel.", overwrites=overwrites, reason=f"Suggestion channel requested by {ctx.author.name}.")
            except discord.Forbidden:
                await ctx.reply("I do not have the required permissions to create a channel.")
                return
            await ctx.reply(f"Text channel created. (<#{channel.id}>)")
        elif channel.lower() == 'remove':
            await utils.setsuggestionchannel(ctx, 'remove')
            await ctx.reply("Successfully removed suggestion channel from the database.")
            return
        else:
            try:
                channel = ctx.guild.get_channel(int(channel.replace('<#','').replace('>','')))
            except ValueError:
                await ctx.reply("Couldn't find that channel.")
                return
            if channel == None:
                await ctx.reply("Couldn't find that channel.")
                return
        await utils.setsuggestionchannel(ctx, channel)
        await ctx.reply(f'Successfully set suggestion channel to <#{channel.id}>.')

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def reports(self, ctx, channel: str=None):
        """ Define a reports channel, or have the bot create one. """
        guild = ctx.guild
        if channel is None:
            await ctx.reply('Please provide a channel.')
            return
        elif channel.lower() == 'create':
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                channel = await guild.create_text_channel('reports', topic="A reports channel.", overwrites=overwrites, reason=f"Suggestion channel requested by {ctx.author.name}.")
            except discord.Forbidden:
                await ctx.reply("I do not have the required permissions to create a channel.")
                return
            await ctx.reply(f"Text channel created. (<#{channel.id}>)")
        elif channel.lower() == 'remove':
            await utils.setreportchannel(ctx, 'remove')
            await ctx.reply("Successfully removed reports channel from the database.")
            return
        else:
            try:
                channel = ctx.guild.get_channel(int(channel.replace('<#','').replace('>','')))
            except ValueError:
                await ctx.reply("Couldn't find that channel.")
                return
            if channel == None:
                await ctx.reply("Couldn't find that channel.")
                return
        await utils.setreportchannel(ctx, channel)
        await ctx.reply(f'Successfully set reports channel to <#{channel.id}>.')

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def counting(self, ctx, channel: str=None):
        """ Define a counting channel, or have the bot create one. """
        guild = ctx.guild
        if channel is None:
            await ctx.reply('Please provide a channel.')
            return
        elif channel.lower() == 'create':
            try:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    guild.me: discord.PermissionOverwrite(read_messages=True, manage_messages=True)
                }
                channel = await guild.create_text_channel('counting', topic="A counting channel.", overwrites=overwrites, reason=f"Counting channel requested by {ctx.author.name}.")
            except discord.Forbidden:
                await ctx.reply("I do not have the required permissions to create a channel.")
                return
            await ctx.reply(f"Text channel created. (<#{channel.id}>)")
        elif channel.lower() == 'remove':
            await utils.setcountingchannel(ctx, 'remove')
            await ctx.reply("Successfully removed counting channel from the database.")
            return
        else:
            try:
                channel = ctx.guild.get_channel(int(channel.replace('<#','').replace('>','')))
            except ValueError:
                await ctx.reply("Couldn't find that channel.")
                return
            if channel == None:
                await ctx.reply("Couldn't find that channel.")
                return
        await utils.setcountingchannel(ctx, channel)
        await ctx.reply(f'Successfully set counting channel to <#{channel.id}>.')

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str=None):
        """ Updates the server's prefix. """
        if prefix is None:
            prefix = '>'
        elif prefix == '':
            await ctx.reply("Invalid argument. Please omit any quotes in the command.")
            return
        await utils.setprefix(ctx, prefix)
        await ctx.reply(f'Successfully changed the server prefix to `{prefix}`')

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def mystbin(self, ctx, setting: bool=None):
        """ Toggle uploading .txt files to Mystbin. """
        if setting is None:
            await ctx.reply("Please provide a setting, either 'on' or 'off'.")
            return
        await utils.mistbin(ctx, setting)
        if setting:
            setting = 'on'
        else: 
            setting = 'off'
        await ctx.reply(f"Successfully toggled MystBin {setting.lower()}.")

    @mystbin.error
    async def eh1(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid argument, either 'on' or 'off'.")

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def token(self, ctx, setting: bool=None):
        """ Toggle token detection on or off. """
        if setting is None:
            await ctx.reply("Please provide a setting, either 'on' or 'off'.")
            return
        await utils.tokenalerter(ctx, setting)
        if setting:
            setting = 'on'
        else: setting = 'off'
        await ctx.reply(f"Successfully toggled Token Detector {setting.lower()}.")

    @token.error
    async def eh2(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid argument, either 'on' or 'off'.")

    @configuration.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def levels(self, ctx, setting: bool=None):
        """ Toggle the guild's Leveling system on or off. """
        if setting is None:
            await ctx.reply("Please provide a setting, either 'on' or 'off'.")
            return
        await utils.levels(ctx, setting)
        if setting:
            setting = 'on'
        else: setting = 'off'
        await ctx.reply(f"Successfully toggled Levels system {setting.lower()}.")

    @levels.error
    async def eh2l(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid argument, either 'on' or 'off'.")

    @commands.group(aliases=['am', 'automod'])
    @commands.has_guild_permissions(manage_guild=True)
    async def automoderation(self, ctx):
        """ Manage automoderation configuration. """
        if ctx.invoked_subcommand is None:
            config = await automod.settings(ctx)
            if config['spam']:
                spam = yes
            else:
                spam = no
            if config['links']:
                links = yes
            else:
                links = no
            if config['swear']:
                swear = yes
            else:
                swear = no
            if config['invites']:
                invites = yes
            else:
                invites = no
            if config['hoisting']:
                hoisting = yes
            else:
                hoisting = no
            color=random.randint(1, 16777215)
            embed = discord.Embed(title="AutoMod Configuration", description=f"""Spam: {spam}
Links: {links}
Swear: {swear}
Invites: {invites}
Hoisting: {hoisting}""", color=color)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)

    @automoderation.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def debug(self, ctx, module: str='all'):
        """ Debug the guild's Automod config """
        module = module.lower()
        user = ctx.guild.get_member(self.bot.user.id)
        if module == 'spam':
            if user.guild_permissions.manage_messages:
                delmsgs = yes
            else:
                delmsgs = no
            embed = discord.Embed(title="Automod Debug - Spam", description=f"Manage Messages: {delmsgs}")
        elif module == 'links':
            if user.guild_permissions.manage_messages:
                delmsgs = yes
            else:
                delmsgs = no
            embed = discord.Embed(title="Automod Debug - Links", description=f"Manage Messages: {delmsgs}")
        elif module == 'swear':
            if user.guild_permissions.manage_messages:
                delmsgs = yes
            else:
                delmsgs = no
            if user.guild_permissions.manage_nicknames:
                mngnicks = yes
            else:
                mngnicks = no
            embed = discord.Embed(title="Automod Debug - Swear", description=f"Manage Messages: {delmsgs}\nManage Nicknames: {mngnicks}")
        elif module == 'invites':
            if user.guild_permissions.manage_messages:
                delmsgs = yes
            else:
                delmsgs = no
            embed = discord.Embed(title="Automod Debug - Invites", description=f"Manage Messages: {delmsgs}")
        elif module == 'hoisting':
            if user.guild_permissions.manage_nicknames:
                mngnicks = yes
            else:
                mngnicks = no
            embed = discord.Embed(title="Automod Debug - Hoisting", description=f"Manage Nicknames: {mngnicks}")
        elif module == 'all':
            if user.guild_permissions.manage_messages:
                delmsgs = yes
            else:
                delmsgs = no
            if user.guild_permissions.manage_nicknames:
                mngnicks = yes
            else:
                mngnicks = no
            embed = discord.Embed(title="Automod Debug", description=f"Manage Messages: {delmsgs}\nManage Nicknames: {mngnicks}")
        else:
            await ctx.reply("Invalid automod module.")
            return
        await ctx.reply(embed=embed)

    @automoderation.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def spam(self, ctx, setting: bool=None):
        """ Toggle the AntiSpam module on or off. """
        if setting is None:
            await ctx.reply("Please provide a setting, either 'on' or 'off'.")
            return
        await automod.antispam(ctx, setting)
        if setting:
            setting = 'on'
        else: 
            setting = 'off'
        await ctx.reply(f"Successfully toggled Antispam {setting.lower()}.")

    @spam.error
    async def eh3(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid argument, either 'on' or 'off'.")

    @automoderation.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def links(self, ctx, setting: bool=None):
        """ Toggle the AntiLinks module on or off. """
        if setting is None:
            await ctx.reply("Please provide a setting, either 'on' or 'off'.")
            return
        await automod.antilinks(ctx, setting)
        if setting:
            setting = 'on'
        else: 
            setting = 'off'
        await ctx.reply(f"Successfully toggled Anti Links {setting.lower()}.")

    @links.error
    async def eh4(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid argument, either 'on' or 'off'.")

    @automoderation.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def swear(self, ctx, setting: bool=None):
        """ Toggle the AntiSwear module on or off. """
        if setting is None:
            await ctx.reply("Please provide a setting, either 'on' or 'off'.")
            return
        await automod.antiswear(ctx, setting)
        if setting:
            setting = 'on'
        else: 
            setting = 'off'
        await ctx.reply(f"Successfully toggled Anti Swear {setting.lower()}.")

    @swear.error
    async def eh5(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid argument, either 'on' or 'off'.")

    @automoderation.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def invites(self, ctx, setting: bool=None):
        """ Toggle the AntiInvites module on or off. """
        if setting is None:
            await ctx.reply("Please provide a setting, either 'on' or 'off'.")
            return
        await automod.antiinvites(ctx, setting)
        if setting:
            setting = 'on'
        else: 
            setting = 'off'
        await ctx.reply(f"Successfully toggled Anti Invites {setting.lower()}.")

    @invites.error
    async def eh6(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid argument, either 'on' or 'off'.")

    @automoderation.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def hoisting(self, ctx, setting: bool=None):
        """ Toggle the AntiHoisting module on or off. """
        if setting is None:
            await ctx.reply("Please provide a setting, either 'on' or 'off'.")
            return
        await automod.antihoist(ctx, setting)
        if setting:
            setting = 'on'
        else: 
            setting = 'off'
        await ctx.reply(f"Successfully toggled Hoist Detection {setting.lower()}.")

    @hoisting.error
    async def eh7(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid argument, either 'on' or 'off'.")

def setup(bot):
    bot.add_cog(Configuration(bot))