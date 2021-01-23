import discord
from discord.ext import commands
from core.ModCore import *
from better_profanity import profanity
from core.AutoModSettings import AutoModSettingsManager
import re

url_regex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

modcore = Mod()
automod = AutoModSettingsManager()

async def poscheck(self, message):
    guild = message.guild
    member = message.author
    if member.guild_permissions.administrator:
        return False
    mempos = member.top_role.position
    me = guild.get_member(self.bot.user.id)
    mepos = me.top_role.position
    if mempos >= mepos:
        return False
    elif guild.owner == member:
        return False
    elif message.author == me:
        return False
    elif mempos > mepos:
        return False
    return True

async def antispam(self, message):
    counter = 0
    with open("automod\\messages.txt", 'r') as file:
        content = file.read()
    with open("automod\\messages.txt", 'a') as file:
        lines = content.split('\n')
        for line in lines:
            if line == str(message.author.id):
                counter +=1
        file.writelines(f"{str(message.author.id)}\n")
        if counter >= 5:
            with open("automod\\messages.txt", 'w') as file:
                content = content.replace(str(message.author.id), '')
            channel = message.channel
            member = message.author
            if await poscheck(self, message):
                try:
                    warns = modcore.warn(message, member, self.bot.user, 'Automod: Spam')
                except error.Unable as e:
                    return
                try:
                    await message.delete()
                    await channel.send(f"{member.mention}, Please stop spamming. This is your {warns} warning.", delete_after=5)
                except discord.Forbidden:
                    pass
                except discord.NotFound:
                    pass

async def antilinks(self, message):
    msg = message.content.lower()
    urls = [url for url in url_regex.findall(message.content)]
    if urls and not message.author.bot:
        if await poscheck(self, message):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, Please do not post links.", delete_after=5)
            except discord.Forbidden:
                pass
            except discord.NotFound:
                pass

async def antiinv(self, message):
    msg = message.content.lower()
    if 'discord.gg/' in msg or 'discord.id/' in msg or 'invite.gg/' in msg:
        if await poscheck(self, message):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, Please do not post server invites.", delete_after=5)
            except discord.Forbidden:
                pass
            except discord.NotFound:
                pass

async def antiswear(self, message):
    msg = message.content.lower()
    if profanity.contains_profanity(msg):
        if await poscheck(self, message):
            try:
                await message.delete()
                await message.channel.send(f"{message.author.mention}, Please do not swear.", delete_after=5)
            except discord.Forbidden:
                pass
            except discord.NotFound:
                pass

async def antiswearname(self, after):
    member = after
    i = False
    try:
        if profanity.contains_profanity(member.nick):
            i = True
    except AttributeError:
        pass
    try:
        if profanity.contains_profanity(member.name):
            i = True
    except AttributeError:
        pass
    if i:
        try:
            await member.edit(nick='No Swearing')
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass

async def antihoist(self, member):
    i = False
    try:
        if member.nick.startswith("!"):
            i = True
    except AttributeError:
        pass
    try:
        if member.name.startswith("!"):
            i = True
    except AttributeError:
        pass
    if i:
        try:
            await member.edit(nick='No Hoisting')
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if await automod.antispamon(message.guild.id):
                await antispam(self, message)
            if await automod.antilinkson(message.guild.id):
                await antilinks(self, message)
            if await automod.antiswearon(message.guild.id):
                await antiswear(self, message)
            if await automod.antiinviteson(message.guild.id):
                await antiinv(self, message)
        except AttributeError:
            pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if await automod.antihoiston(after.guild.id):
            await antihoist(self, after)
        if await automod.antiswearon(after.guild.id):
            await antiswearname(self, after)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await automod.antihoiston(member.guild.id):
            await antihoist(self, member)
        if await automod.antiswearon(member.guild.id):
            await antiswearname(self, member)

def setup(bot):
    bot.add_cog(AutoMod(bot))