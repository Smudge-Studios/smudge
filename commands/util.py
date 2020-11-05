import discord
from discord.ext import commands
from core.UtilCore import *
from core.Exceptions import *
import datetime

utils = Utils()

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """ Check the bot's latency. """
        msg = await ctx.send('Pong!')
        ms = (msg.created_at-ctx.message.created_at).total_seconds() * 1000
        await msg.edit(content=f"Pong!  `{int(ms)}ms`")
    
    @commands.command()
    @commands.bot_has_permissions(read_message_history=True)
    async def report(self, ctx, member: discord.Member=None, *, reason: str=None):
        try:
            await ctx.message.delete(delay=None)
        except discord.Forbidden:
            pass
        if member is None:
            await ctx.send("Please provide a user to report.")
            return
        if reason is None:
            await ctx.send(f"Please provide a reason for reporting {member.name}.")
            return
        try:
            channel = utils.reportchannel(ctx)
        except error.Unable as e:
            await ctx.send(str(e))
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
        embed = discord.Embed(title="User Report", description=f"User: <@{member.id}>\nReason:{reason}\n[Jump to message]({url})")
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
        try:
            await channel.send(embed=embed)
            r = await ctx.send("Thank you, I have forwarded your report to server staff.")
            await r.delete(delay=3.0)
        except discord.Forbidden:
            await ctx.send("Sorry, I can't send messages in the report channel. Please contact a server administrator to fix this issue.")

    @commands.command()
    async def suggest(self, ctx, *, suggestion: str=None):
        if suggestion is None:
            await ctx.send("Please provide a suggestion.")
            return
        try:
            channel = utils.suggestchannel(ctx)
            channel = ctx.guild.get_channel(channel)
        except error.Unable as e:
            await ctx.send(str(e))
            return
        embed = discord.Embed(title="Suggestion", description=f"{suggestion}")
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=f"{ctx.author.avatar_url}")
        try:
            message = await channel.send(embed=embed)
            await message.add_reaction('\N{THUMBS UP SIGN}')
            await message.add_reaction('\N{THUMBS DOWN SIGN}')
        except discord.Forbidden:
            await ctx.send(f"Sorry, I can't send messages in <#{channel.id}>. Please contact a server administrator to fix this issue.")
            return
        await ctx.send(f"Thank you for your suggestion, it has been posted in <#{channel.id}>")

    @commands.command('memberinfo')
    async def userinfo(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"Info on {member.name}#{member.discriminator}")
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
        year = created.year
        month = created.month
        day = created.day
        embed.add_field(name="Joined at", value=f"{month}/{day}/{year}")
        embed.set_thumbnail(url=member.avatar_url)

    @commands.command(aliases=['guildinfo'])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Information")
        embed.add_field(name="Name", value=guild.name, inline=True)
        embed.add_field(name="ID", value=str(guild.id), inline=True)
        embed.add_field(name="Owner", value=f"{guild.owner.name}#{guild.owner.discriminator}", inline=True)
        
        embed.add_field(name="Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.member_count)), inline=True)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        
        embed.add_field(name="Boost Level", value=str(guild.premium_tier), inline=True)
        embed.add_field(name="Nitro Boosts", value=str(guild.premium_subscription_count), inline=True)
        embed.add_field(name="Boosters", value=str(len(guild.premium_subscribers)), inline=True)
        
        embed.add_field(name="Region", value=guild.region, inline=True)

        embed.set_image(url=guild.icon_url)


def setup(bot):
    bot.add_cog(Util(bot))