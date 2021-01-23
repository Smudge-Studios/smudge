import random
from core.ModCore import *
import discord
from discord.ext import commands
import time
import asyncio
import aiosqlite

modcore = Mod()

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def muterole(self, ctx, role, name: str=None):
        """ Specify a mute role, or have the bot create one. """
        guild = ctx.guild
        muterole = None
        if role.lower() == 'create':
            async with ctx.channel.typing():
                if name == None:
                    await ctx.reply('Please specify the name for your mute role.')
                    return
                fail = 0
                success = 0
                try:
                    perms = discord.Permissions(send_messages=False, read_messages=True)
                    muterole = await guild.create_role(name=name, permissions=perms, reason=f"Muterole requested by {ctx.author}")
                    for channel in guild.channels:
                        try:
                            await channel.set_permissions(muterole, send_messages=False, reason=f"Muterole Overwrites requested by {ctx.author}")
                            success = success+1
                        except discord.Forbidden:
                            fail = fail+1
                except discord.Forbidden:
                    await ctx.reply("Sorry, I do not have enough permissions to create roles.")
                    return
                await ctx.reply(f"Muterole created with overwrites in {success} channels. {fail} channels were skipped.")
        else:
            yes = False
            for role1 in guild.roles:
                if role1.name == role:
                    muterole = role1
                    yes = True
                    break
                yes = False
            if yes is False:
                await ctx.reply(f"Unable to find role {role}.")
                return
            elif yes is True:
                pass
        if muterole is None:
            await ctx.reply(f"Unable to find role {role}.")
            return
        async with aiosqlite.connect('data\\moderation.db') as conn:
         async with conn.execute("SELECT * from CONFIG") as cursor:
            i = False
            async for row in cursor:
                if row[0] == ctx.guild.id:
                    conn.execute(f"UPDATE CONFIG set MUTEROLE = {muterole.id} where GUILD = {guild.id}")
                    i = True
                    break
            if i == False:
                conn.execute(f"INSERT INTO CONFIG (GUILD,MUTEROLE) \
                    VALUES ({guild.id}, {muterole.id})")
            conn.commit()
        await ctx.reply(f"Successfully set the muterole to {muterole.name}.")
            
    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member=None, reason: str='None'):
        """ Sends a warning to a user. """
        if member is None:
            await ctx.reply("Please provide a member to warn.")
            return
        guild = ctx.guild
        mempos = member.top_role.position
        modpos = ctx.author.top_role.position
        me = guild.get_member(self.bot.user.id)
        mepos = me.top_role.position
        if mempos >= mepos:
            await ctx.reply(f"Unable to warn {member.name} due to role hierarchy.")
            return
        elif guild.owner == member:
            await ctx.reply(f"I cannot warn the guild's owner.")
            return
        elif ctx.author == member:
            await ctx.reply(f"You cannot warn yourself.")
            return
        elif mempos > modpos:
            await ctx.reply(f"You cannot warn {member.name} due to role hierarchy..")
            return
        try:
            warns = await modcore.warn(ctx, member, ctx.author, reason)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        try:
            await member.reply(f"You were warned in {ctx.guild.name}. Reason: {reason}. \nThis is your {warns} warning.")
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass
        await ctx.reply(f"Successfully warned {member.name}. This is their {warns} warning.")
    
    @warn.error
    async def eh999994(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member=None, duration: str=None, *, reason: str='None'):
        """ Mutes someone with an optional duration. """
        now = time.time()
        if member is None:
            await ctx.reply('Please specify a user to mute.')
            return
        guild = ctx.guild
        mempos = member.top_role.position
        modpos = ctx.author.top_role.position
        me = guild.get_member(self.bot.user.id)
        mepos = me.top_role.position
        if mempos >= mepos:
            await ctx.reply(f"Unable to mute {member.name} due to role hierarchy.")
            return
        elif guild.owner == member:
            await ctx.reply(f"I cannot mute the guild's owner.")
            return
        elif ctx.author == member:
            await ctx.reply(f"You cannot mute yourself.")
            return
        elif mempos > modpos:
            await ctx.reply(f"You cannot mute {member.name} due to role hierarchy.")
            return
        try:
            duration = await modcore.gettime(duration)
            expires = now+duration
        except TypeError:
            reason = f"{duration} {reason}"
            if reason == '':
                reason = 'None'
            expires = -1
        try:
            muterole = await modcore.mute(ctx, member, reason, expires)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        try:
            await member.reply(f"You were muted in {guild.name}. Reason: {reason}.")
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass
        await member.add_roles(muterole, reason=f"Muted by {ctx.author.name}. Reason: {reason}")
        await ctx.reply(f"Successfully muted {member.name}: {reason}")

    @mute.error
    async def eh999993(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")
        else:
            raise error

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, duration: str=None, *, reason: str=''):
        """ Bans someone with an optional duration. """
        now = time.time()
        if member is None:
            await ctx.reply('Please specify a user to ban.')
            return
        guild = ctx.guild
        mempos = member.top_role.position
        modpos = ctx.author.top_role.position
        me = guild.get_member(self.bot.user.id)
        mepos = me.top_role.position
        if mempos >= mepos:
            await ctx.reply(f"Unable to ban {member.name} due to role hierarchy.")
            return
        elif guild.owner == member:
            await ctx.reply(f"I cannot ban the guild's owner.")
            return
        elif ctx.author == member:
            await ctx.reply(f"You cannot ban yourself.")
            return
        elif mempos > modpos:
            await ctx.reply(f"You cannot ban {member.name} due to role hierarchy..")
            return
        try:
            duration = await modcore.gettime(duration)
            expires = now+duration
        except:
            reason = f"{duration} {reason}"
            if reason == '':
                reason = 'None'
            expires = -1
        try:
            await modcore.ban(ctx, member, reason, expires)
        except error.Unable as e:
            await ctx.reply(e)
            return
        try:
            await member.reply(f"You were banned from {guild.name}. Reason: {reason}.")
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass
        await guild.ban(member, reason=f"Banned by {ctx.author.name}. Reason: {reason}")
        await ctx.reply(f"Successfully banned {member.name}: {reason}")

    @ban.error
    async def eh999992(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason: str='None'):
        """ Kicks a member. """
        if member is None:
            await ctx.reply('Please specify a user to kick.')
            return
        guild = ctx.guild
        mempos = member.top_role.position
        modpos = ctx.author.top_role.position
        me = guild.get_member(self.bot.user.id)
        mepos = me.top_role.position
        if mempos >= mepos:
            await ctx.reply(f"Unable to kick {member} due to role hierarchy.")
            return
        elif guild.owner == member:
            await ctx.reply(f"I cannot kick the guild's owner.")
            return
        elif ctx.author == member:
            await ctx.reply(f"You cannot ban yourself.")
            return
        elif mempos > modpos:
            await ctx.reply(f"You cannot ban {member} due to role hierarchy..")
            return
        try:
            await modcore.kick(ctx, member, reason)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        try:
            await member.reply(f"You were kicked from {guild.name}. Reason: {reason}.")
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass
        await guild.kick(member, reason=f"Kicked by {ctx.author.name}. Reason: {reason}")
        await ctx.reply(f"Successfully kicked {member}: {reason}")

    @kick.error
    async def eh999991(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, number: str='100'):
        """ Bulk deletes a number of messages in a channel. Limit of 100 messages. """
        try:
            number = int(number)
        except ValueError:
            await ctx.reply(f"Invalid number.")
        if number > 500:
            await ctx.reply(f"Cannot delete more than 500 messages.")
            return
        try:
            number = int(number)
        except ValueError:
            await ctx.reply("Invalid number.")
            return
        deleted = await ctx.channel.purge(limit=number, bulk=True)
        if len(deleted) > 1:
            await ctx.reply(f'Deleted {len(deleted)} messages.', delete_after=5)
        else:
            await ctx.reply(f'Deleted {len(deleted)} message.', delete_after=5)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member: str=None):
        """ Unban the specified user from the guild. """
        guild = ctx.guild
        if member is None:
            await ctx.reply('Please provide a user to unban.')
            return
        try:
            member = discord.Object(id=int(member))
        except ValueError:
            await ctx.reply("Invalid user ID.")
        await modcore.unban(ctx, member)
        try:
            await guild.unban(member, reason=f"Unbanned by {ctx.author.name}.")
        except discord.NotFound:
            await ctx.reply("That user is not banned.")
            return
        await ctx.reply(f"Successfully unbanned the specified user.")

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member=None):
        """ Unmutes the specified user. """
        guild = ctx.guild
        if member is None:
            await ctx.reply('Please provide a user to unmute.')
            return
        try:
            muterole = await modcore.unmute(ctx, member)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        await member.remove_roles(muterole, reason=f"Unmuted by {ctx.author.name}.")
        try:
            await member.reply(f'You were unmuted by {ctx.author.name} in {guild.name}.')
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass
        await ctx.reply(f"Successfully unmuted {member}.")

    @unmute.error
    async def eh992999(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command(aliases=['listpunish', 'lpunish', 'infractions', 'lp'])
    @commands.has_guild_permissions(manage_guild=True)
    async def listpunishments(self, ctx, member: discord.Member=None, type: str=None):
        """ Displays a list of punishments a member has recieved. """
        color=random.randint(1, 16777215)
        if member is None:
            await ctx.reply("Please specify a member.")
            return
        try:
            ids, reasons, types = await modcore.fetchpunishlist(ctx, member, type)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        x = 0
        ps = ''
        for i in ids:
            ps = ps+f"Type: {types[x]} - Id: {i} - Reason: {reasons[x]}\n"
            x = x+1
        embed = discord.Embed(title=f"Punishments for {member}", description=ps, color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
        
    @listpunishments.error
    async def eh99999111(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command(aliases=['punish','punishinfo','infraction','pi'])
    @commands.has_guild_permissions(manage_guild=True)
    async def punishmentinfo(self, ctx, id: str=None):
        """ Displays information on a specific punishment. """
        color=random.randint(1, 16777215)
        if id is None:
            await ctx.reply("Please provide a punishment ID.")
            return
        try:
            id = int(id)
        except ValueError:
            await ctx.reply(f"Invalid punishment ID.")
            return
        try:
            data, type = await modcore.fetchpunish(ctx, id)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        member = self.bot.get_user(data[1])
        mod = self.bot.get_user(data[3])
        embed = discord.Embed(title=f"Information on punishment {id}", description=f"""User: {member}
Punishment Type: {type}
Moderator: {mod}
Reason: {data[2]}""", color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['delpunish','deletepunish', 'dp'])
    @commands.has_guild_permissions(manage_guild=True)
    async def deletepunishment(self, ctx, id: int=None):
        """ Deletes a punishment. This action is irreversable. """
        if id is None:
            await ctx.reply("Please provide a punishment ID.")
            return
        try:
            await modcore.fetchpunish(ctx, id)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        msg = await ctx.reply("Are you sure you want to proceed with this action? Deleting a punishment may have unexpected consequences.")
        await msg.add_reaction('a:greenTick:784137919422005249')
        await msg.add_reaction('a:redTick:784137915269382185')
        def check(reaction, user):
            if str(reaction.emoji) == '<a:greenTick:784137919422005249>':
                if reaction.message == msg:
                    return user == ctx.author
            elif str(reaction.emoji) == '<a:redTick:784137915269382185>':
                if user == ctx.author:
                    if reaction.message == msg:
                        raise error.Unable(f"Operation cancelled.")
        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.reply('Operation timed out.')
            return
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        try:
            await modcore.delpunish(ctx, id)
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        await ctx.reply("The operation was a success.")

    @deletepunishment.error
    async def eh9999t567568y59(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide a valid punishment ID.")

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def clearwarns(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.reply("Please provide a member.")
            return
        ids, resons, types = await modcore.faetchpunishlist(ctx, member, 'WARNS')
        if len(ids) == 0:
            await ctx.reply(f"{member} has no warnings.")
            return
        msg = await ctx.reply("Are you sure you want to proceed with this action?")
        await msg.add_reaction('a:greenTick:784137919422005249')
        await msg.add_reaction('a:redTick:784137915269382185')
        def check(reaction, user):
            if str(reaction.emoji) == '<a:greenTick:784137919422005249>':
                return user == ctx.author
            elif str(reaction.emoji) == '<a:redTick:784137915269382185>':
                if user == ctx.author:
                    raise error.Unable(f"Operation cancelled.")
        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.reply('Operation timed out.')
            return
        except error.Unable as e:
            await ctx.reply(str(e))
            return
        for _id in ids:
            await modcore.delpunish(ctx, _id)
        await ctx.reply(f"Successfully cleared warnings for {member}.")

    @clearwarns.error
    async def eh9999ey59(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

def setup(bot):
    bot.add_cog(Moderation(bot))