import discord
from discord.ext import commands
from core.UtilCore import *
from core.Exceptions import *
import random
import re
from aiohttp import ClientSession

utils = Utils()

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession()

    @commands.command()
    async def ping(self, ctx):
        """ Check the bot's latency. """
        msg = await ctx.reply('Pong!')
        ms = (msg.created_at-ctx.message.created_at).total_seconds() * 1000
        await msg.edit(content=f"Pong!  `{int(ms)}ms`")
    
    @commands.command()
    @commands.bot_has_permissions(read_message_history=True)
    async def report(self, ctx, member: discord.Member=None, *, reason: str=None):
        """ Report a user for violation of server rules. """
        try:
            await ctx.message.delete(delay=None)
        except discord.Forbidden:
            pass
        if member is None:
            await ctx.reply("Please provide a user to report.")
            return
        if reason is None:
            await ctx.reply(f"Please provide a reason for reporting {member.name}.")
            return
        try:
            channel = await utils.reportchannel(ctx)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        msg = None
        async for message in channel.history(limit=200):
            if message.author == member:
                msg = message
                break
        if msg is None:
            url = ctx.message.jump_url
        else:
            url = msg.jump_url
        color=random.randint(1, 16777215)
        embed = discord.Embed(title="User Report", description=f"User: {member}\nReason: {reason}\n[Jump to message]({url})", color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        try:
            await channel.reply(embed=embed)
            r = await ctx.reply("Thank you, I have forwarded your report to server staff.")
            await r.delete(delay=3.0)
        except discord.Forbidden:
            await ctx.reply("Sorry, I can't send messages in the report channel. Please contact a server administrator to fix this issue.")

    @report.error
    async def eh999757499(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command()
    async def suggest(self, ctx, *, suggestion: str=None):
        """ Make a suggestion to the server. """
        if suggestion is None:
            await ctx.reply("Please provide a suggestion.")
            return
        try:
            channel = await utils.suggestchannel(ctx)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        color=random.randint(1, 16777215)
        embed = discord.Embed(title="Suggestion", description=f"{suggestion}", color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        try:
            message = await channel.reply(embed=embed)
            await message.add_reaction('\N{THUMBS UP SIGN}')
            await message.add_reaction('\N{THUMBS DOWN SIGN}')
        except discord.Forbidden:
            await ctx.reply(f"Sorry, I can't send messages in <#{channel.id}>. Please contact a server administrator to fix this issue.")
            return
        await ctx.reply(f"Thank you for your suggestion, it has been posted in <#{channel.id}>")

    @commands.command(aliases=['memberinfo'])
    async def userinfo(self, ctx, member: discord.Member=None):
        """ Displays information on a user, or yourself if no user is specified. """
        color=random.randint(1, 16777215)
        if member is None:
            member = ctx.author
        if member.bot:
            name = f"{member} [BOT]"
        else:
            name = f"{member}"
        embed = discord.Embed(title=f"Info on {name}", color=color)
        embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
        embed.add_field(name="Nick", value=member.nick, inline=True)
        embed.add_field(name="ID", value=str(member.id), inline=True)
        created = member.created_at
        year = created.year
        month = created.month
        day = created.day
        embed.add_field(name="Created at", value=f"{month}/{day}/{year}")
        joined = member.joined_at
        year = joined.year
        month = joined.month
        day = joined.day
        embed.add_field(name="Joined at", value=f"{month}/{day}/{year}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @userinfo.error
    async def eh99436547547999(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member: discord.Member=None):
        """ Displays a user's avatar. """
        color=random.randint(1, 16777215)
        if member is None:
            member = ctx.author
        if member.is_avatar_animated == True:
            embed=discord.Embed(title=f"{member}'s Avatar", color=color)
            embed.add_field(name="Link as", value=f"[gif]({member.avatar_url_as(format='gif')})")
        else:
            embed=discord.Embed(title=f"{member}'s Avatar", color=color)
            embed.add_field(name="Link as", value=f"[webp]({member.avatar_url_as(format='webp')}) | [jpg]({member.avatar_url_as(format='jpg')}) | [png]({member.avatar_url_as(format='png')})", inline=True)
        embed.set_image(url=member.avatar_url)
        await ctx.reply(embed=embed)

    @avatar.error
    async def eh99999557(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command(aliases=['guildinfo'])
    async def serverinfo(self, ctx):
        """ Displays information on the guild the command was ran in. """
        guild = ctx.guild
        color=random.randint(1, 16777215)
        members = guild.members
        total = 0
        bots = 0
        humans = 0
        for e in members:
            total += 1
            if e.bot:
                bots += 1
            else:
                humans += 1
        embed = discord.Embed(title=f"Server Information", color=color)
        embed.add_field(name="Guild", value=f"Name: {guild.name}\nID: {guild.id}\nRegion: {guild.region}", inline=True)
        embed.add_field(name="Owner", value=f"{guild.owner}", inline=True)
        embed.add_field(name="Boosts", value=f"Level: {guild.premium_tier}\nBoosters: {len(guild.premium_subscribers)}\nTotal Boosts: {guild.premium_subscription_count}", inline=True)
        
        embed.add_field(name="Roles", value=f"Roles: {len(guild.roles)}", inline=True)
        embed.add_field(name="Members", value=f"Total: {guild.member_count}\nHumans: {humans}\nBots: {bots}", inline=True)
        embed.add_field(name="Channels", value=f"Total: {len(guild.channels)}\nText: {len(guild.text_channels)}\nVoice: {len(guild.voice_channels)}", inline=True)
    

        embed.set_thumbnail(url=guild.icon_url)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def poll(self, ctx, *, input: str=None):
        """ Create a poll with a maximum of 5 answers.
            Usage: poll question | option 1 | option 2 | etc. """
        if input is None:
            await ctx.reply("Please provide a question and answers.")
            return
        a = '\N{REGIONAL INDICATOR SYMBOL LETTER A}'
        b = '\N{REGIONAL INDICATOR SYMBOL LETTER B}'
        c = '\N{REGIONAL INDICATOR SYMBOL LETTER C}'
        d = '\N{REGIONAL INDICATOR SYMBOL LETTER D}'
        e = '\N{REGIONAL INDICATOR SYMBOL LETTER E}'
        try:
            question, options = await utils.poll(input)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        msg = f'{question}\n\n'
        if len(options) == 2:
            msg = msg+f'{a}: {options[0]}\n{b}: {options[1]}'
        elif len(options) == 3:
            msg = msg+f'{a}: {options[0]}\n{b}: {options[1]}\n{c}: {options[2]}'
        elif len(options) == 4:
            msg = msg+f'{a}: {options[0]}\n{b}: {options[1]}\n{c}: {options[2]}\n{d}: {options[3]}'
        else:
            msg = msg+f'{a}: {options[0]}\n{b}: {options[1]}\n{c}: {options[2]}\n{d}: {options[3]}\n{e}: {options[4]}'
        color=random.randint(1, 16777215)
        embed = discord.Embed(title="Poll", description = msg, color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        try:
            poll = await ctx.reply(embed=embed)
        except discord.Forbidden:
            await ctx.author.reply("Sorry, I cannot send/embed messages in that channel.")
            return
        try:
            if len(options) == 2:
                await poll.add_reaction(a)
                await poll.add_reaction(b)
            elif len(options) == 3:
                await poll.add_reaction(a)
                await poll.add_reaction(b)
                await poll.add_reaction(c)
            elif len(options) == 4:
                await poll.add_reaction(a)
                await poll.add_reaction(b)
                await poll.add_reaction(c)
                await poll.add_reaction(d)
            else:
                await poll.add_reaction(a)
                await poll.add_reaction(b)
                await poll.add_reaction(c)
                await poll.add_reaction(d)
                await poll.add_reaction(e)
        except discord.Forbidden:
            await poll.edit("Sorry, I cannot add reactions in this channel.")

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def quickpoll(self, ctx, *, question):
        """ Create a quick and simple yes/no poll. """
        if input is None:
            await ctx.reply("Please provide a question and answers.")
            return
        yes = ":upvote:781603344397500416"
        no = ":downvote:781603346204327947"
        color=random.randint(1, 16777215)
        embed = discord.Embed(title="Poll", description=f"{question}\n<{yes}>: Yes\n<{no}>: No", color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        try:
            poll = await ctx.reply(embed=embed)
        except discord.Forbidden:
            await ctx.author.reply("Sorry, I cannot send/embed messages in that channel.")
            return
        try:
            await poll.add_reaction(yes)
            await poll.add_reaction(no)
        except discord.Forbidden:
            await poll.edit("Sorry, I cannot add reactions in this channel.")

    @commands.command()
    async def info(self, ctx):
        """ Displays some somewhat useful information. """
        color=random.randint(1, 16777215)
        embed = discord.Embed(title="Pretty much useless information", description="""Unbans and Unmutes are only checked once a minute.
Messages for the guild's leveling system are only counted when they give the user XP.
Automod will always ignore members with a higher role than the bot, and will ignore members with the Administrator permission.
This bot is probably very useful but overengineered.""", color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command()
    async def prefix(self, ctx):
        """ Displays the bot's set prefix. """
        prefix = await utils.get_readable_prefix(ctx)
        await ctx.reply(f"My prefix in this server is `{prefix}`.")
        
    @commands.command(aliases=['ds'])
    async def discordstatus(self, ctx):
        """ Displays the current Discord status. """
        color=random.randint(1, 16777215)
        async with self.session.get("https://discordstatus.com/history.json") as response:
            data = await response.json()
        embed = discord.Embed(title="Hypixel Status", description = f"{data['components'][0]['name']}: {data['components'][0]['status'].capitalize()}\n" +
        f"{data['components'][1]['name']}: {data['components'][1]['status'].capitalize()}\n" +
        f"{data['components'][2]['name']}: {data['components'][2]['status'].capitalize()}\n" + 
        f"{data['components'][3]['name']}: {data['components'][3]['status'].capitalize()}\n" +
        f"{data['components'][4]['name']}: {data['components'][4]['status'].capitalize()}", color=color)
        updat = data['page_status']['page']['updated_at'].split('T')
        updatd2 = updat[1].split('.')[0]
        try:
            current = data["months"][0]["incidents"][0]
            timestamp = re.sub(r"<var data-var='date'>|</var>|<var data-var='time'>", "", current["timestamp"])
            if 'been resolved' in current['message'].lower():
                raise IndexError
            embed.add_field(name=f"{current['name']}", description=f"{current['message']}\nImpact: {current['impact'].capitalize()}\nIncident created {timestamp}", color=color)
        except IndexError:
            pass
        embed.set_footer(text=f"Status updated {updat[0]} at {updatd2}")
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Utility(bot))