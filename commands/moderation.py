from core.ModCore import *
import discord
from discord.ext import commands
import sqlite3
import time

conn = sqlite3.connect('data\\moderation.db')
modcore = Mod()

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command
    @commands.has_guild_permissions(manage_guild=True)
    async def muterole(self, ctx, role, name: str=None):
        """ Specify a mute role, or have the bot create one. """
        guild = ctx.guild
        if role.lower() == 'create':
            if name == None:
                await ctx.send('Please specify the name for your mute role.')
                return
            fail = 0
            success = 0
            try:
                perms = discord.Permissions(send_messages=False, read_messages=True)
                muterole = await guild.create_role(name=name, permissions=perms, reason=f"Muterole requested by {ctx.author.name}")
                await ctx.send(f"Muterole created.")
                for channel in guild.channels:
                    try:
                        perms = channel.overwrites_for(muterole)
                        perms.send_messages = False
                        await channel.set_permissions(muterole, overwrites=perms, reason=f'MuteRole overwrites for role {muterole.name}.')
                        success = success+1
                    except discord.Forbidden:
                        fail = fail+1
            except discord.Forbidden:
                await ctx.send("Sorry, I do not have enough permissions to create roles.")
                return
            await ctx.send(f"Muterole overwrites were created in {success} channels. {fail} channels were skipped.")
        else:
            yes = False
            for role in guild.roles:
                if role.name == role:
                    muterole = role
                    yes = True
                    break
                yes = False
            if yes is False:
                await ctx.send(f"Unable to find role {role}.")
                return
            elif yes is True:
                pass
        cursor = conn.execute("SELECT * from CONFIG")
        try:
            i = False
            for row in cursor:
                if row[0] == ctx.guild.id:
                    conn.execute(f"UPDATE CONFIG set MUTEROLE = {muterole.id} where GUILD = {guild.id}")
                    i = True
                    break
            if i == False:
                raise ValueError
        except ValueError:
            conn.execute(f"INSERT INTO CONFIG (GUILD,MUTEROLE) \
                VALUES ({guild.id}, {muterole.id}, 0)")
        await ctx.send(f"Successfully set the muterole to {muterole.name}.")
            
    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member=None, reason: str='None'):
        """ Sends a warning to a user. """
        if member is None:
            await ctx.send("Please provide a member to warn.")
            return
        try:
            warns = modcore.warn(ctx, member, reason)
        except error.Unable as e:
            await ctx.send(str(e))
            return
        try:
            await member.send(f"You were warned in {ctx.guild.name}. Reason: {reason}. \nThis is your {warns} warning.")
        except discord.Forbidden:
            pass
        await ctx.send(f"Successfully warned {member.name}. This is their {warns} warning.")
    
    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member=None, duration: str=None, *, reason: str='None'):
        """ Mutes someone with an optional duration. """
        guild = ctx.guild
        now = time.time()
        if member is None:
            await ctx.send('Please specify a user to mute.')
            return
        try:
            duration = modcore.gettime(duration)
            expires = now+duration
        except ValueError:
            reason = duration+reason
            expires = 'Permanent'
        try:
            muterole = modcore.mute(ctx, member, reason, expires)
        except error.Unable as e:
            await ctx.send(str(e))
            return
        try:
            await member.send(f"You were muted in {guild.name}. Reason: {reason}.")
        except discord.Forbidden:
            pass
        await member.add_roles(muterole, reason=f"Muted by {ctx.author.name}. Reason: {reason}")

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, duration: str=None, *, reason: str='None'):
        """ Bans someone with an optional duration. """
        guild = ctx.guild
        now = time.time()
        if member is None:
            await ctx.send('Please specify a user to ban.')
            return
        try:
            duration = modcore.gettime(duration)
            expires = now+duration
        except ValueError:
            reason = duration+reason
            expires = 'Permanent'
        try:
            modcore.ban(ctx, member, reason, expires)
        except error.Unable as e:
            await ctx.send(e)
            return
        try:
            await member.send(f"You were banned from {guild.name}. Reason: {reason}.")
        except discord.Forbidden:
            pass
        await guild.ban(member, reason=f"Banned by {ctx.author.name}. Reason: {reason}")

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason: str='None'):
        """ Kicks a member. """
        guild = ctx.guild
        if member is None:
            await ctx.send('Please specify a user to kick.')
            return
        try:
            modcore.kick(ctx, member, reason)
        except error.Unable as e:
            await ctx.send(str(e))
            return
        try:
            await member.send(f"You were kicked from {guild.name}. Reason: {reason}.")
        except discord.Forbidden:
            pass
        await guild.kick(member, reason=f"Kicked by {ctx.author.name}. Reason: {reason}")

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, number: str='100'):
        """ Bulk deletes a number of messages in a channel. Limit of 100 messages. """
        if number > 1000:
            await ctx.send(f"Cannot delete more than 1000 messages.")
            return
        try:
            number = int(number)
        except ValueError:
            await ctx.send("Invalid number.")
            return
        deleted = await ctx.channel.purge(limit=number, check=True)
        if len(deleted) > 1:
            await ctx.send(f'Deleted {len(deleted)} messages.')
        else:
            await ctx.send(f'Deleted {len(deleted)} message.')

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member=None):
        """ Unban the specified user from the guild. """
        guild = ctx.guild
        if member is None:
            await ctx.send('Please provide a user to unban.')
            return
        banlist = await guild.bans()
        if member not in banlist:
            await ctx.send(f"{member.name} is not banned.")
            return
        modcore.unban(ctx, member)
        await guild.unban(member, reason=f"Unbanned by {ctx.author.name}.")
        await ctx.send(f"Successfully unbanned {member.name}.")

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member=None):
        """ Unmutes the specified user. """
        guild = ctx.guild
        if member is None:
            await ctx.send('Please provide a user to unmute.')
            return
        try:
            muterole = modcore.unmute(ctx, member)
        except error.Unable as e:
            await ctx.send(str(e))
            return
        member.remove_roles(muterole, reason=f"Unmuted by {ctx.author.name}.")
        try:
            await member.send(f'You were unmuted by {ctx.author.name} in {guild.name}.')
        except discord.Forbidden:
            pass
        await ctx.send(f"Successfully unmuted {member.name}.")

    @commands.command(aliases=['listpunish', 'lpunish', 'infractions', 'lp'])
    @commands.has_guild_permissions(manage_guild=True)
    async def listpunishments(self, ctx, member: discord.Member=None, type: str=None):
        """ Displays a list of punishments a member has recieved. """
        if member is None:
            await ctx.send("Please specify a member.")
            return
        try:
            ids, reasons, types = modcore.fetchpunishlist(ctx, member, type)
        except error.Unable as e:
            await ctx.send(str(e))
            return
        x = 0
        ps = ''
        for i in ids:
            ps = ps+f"Type: {types[x]} - Id: {i} - Reason: {reasons[x]}\n"
            x = x+1
        embed = discord.Embed(title=f"Punishments for {member.name}", description=ps)
        
    @commands.command(aliases=['punish','punishinfo','infraction','pi'])
    @commands.has_guild_permissions(manage_guild=True)
    async def punishmentinfo(self, ctx, id: str=None):
        """ Displays information on a specific punishment. """
        if id is None:
            await ctx.send("Please provide a punishment ID.")
            return
        try:
            id = int(id)
        except ValueError:
            await ctx.send(f"Invalid punishment ID.")
        try:
            data, type = modcore.fetchpunish(ctx, id)
        except error.Unable as e:
            await ctx.send(str(e))
            return
        member = self.bot.get_member(data[1])
        mod = self.bot.get_member(data[3])
        embed = discord.Embed(title=f"Information on punishment {id}", description=f"""User: <@{member.id}>
        Punishment Type: {type}
        Moderator: <@{mod.id}>
        Reason: {data[2]}""")
        await ctx.send(embed=embed)

    @commands.command(aliases=['delpunish','deletepunish', 'dp'])
    @commands.has_guild_permissions(manage_guild=True)
    async def deletepunishment(self, ctx, id: int=None):
        """ Deletes a punishment. This action is irreversable. """
        if id is None:
            await ctx.send("Please provide a punishment ID.")
            return
        try:
            modcore.fetchpunish(id)
        except error.Unable as e:
            await ctx.send(str(e))
        await ctx.send("Are you sure you want to proceed with this action? Deleting a punishment may have unexpected consequences.")
        def check(reaction, user):
            if str(reaction.emoji) == '✅':
                return user == ctx.author
            elif str(reaction.emoji) == '❎':
                raise error.Unable(f"Operation cancelled.")
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Operation timed out.')
            return
        except error.Unable as e:
            await ctx.send(str(e))
            return
        try:
            modcore.delpunish(id)
        except error.Unable as e:
            await ctx.send(str(e))
            return
        await ctx.send("The operation was a success.")

def setup(bot):
    bot.add_cog(Moderation(bot))