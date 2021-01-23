import discord
from discord.ext import commands
import random

yes = '<a:greenTick:784137919422005249>'
no = '<a:redTick:784137915269382185>'

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role(self, ctx):
        """ Does nothing without a subcommand. """
        if ctx.invoked_subcommand is None:
            await ctx.reply_help('role')

    @role.command()
    async def add(self, ctx, role: str=None, member: discord.Member=None):
        """ Add a role to a member. """
        if role is None:
            await ctx.reply("Please provide a role.")
            return
        if member is None:
            await ctx.reply("Please provide a member.")
            return
        role = role.replace('<@&', '').replace('>', '')
        _role = None
        try:
            role = int(role)
            _role = ctx.guild.get_role(role)
        except:
            role = role.lower()
            for role1 in ctx.guild.roles:
                role11 = role1.name
                if role11.lower() == role:
                    _role = role1
                    break
        if _role is None:
            await ctx.reply("Invalid role.")
            return
        try:
            await member.add_roles(_role, reason=f"Added by {ctx.author}")
        except discord.HTTPException:
            await ctx.reply(f"Couldn't add {_role.name} to {member}.")
            return
        await ctx.reply(f"Successfully added {_role.name} to {member}.")
        
    @add.error
    async def adderrh(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid member.")

    @role.command(aliases=['rem'])
    async def remove(self, ctx, role: str=None, member: discord.Member=None):
        """ Remove a role from a member. """
        if role is None:
            await ctx.reply("Please provide a role.")
            return
        if member is None:
            await ctx.reply("Please provide a member.")
            return
        role = role.replace('<@&', '').replace('>', '')
        _role = None
        try:
            role = int(role)
            _role = ctx.guild.get_role(role)
        except:
            role = role.lower()
            for role1 in ctx.guild.roles:
                role11 = role1.name
                if role11.lower() == role:
                    _role = role1
                    break
        if _role is None:
            await ctx.reply("Invalid role.")
            return
        try:
            await member.remove_roles(_role, reason=f"Removed by {ctx.author}")
        except discord.HTTPException:
            await ctx.reply(f"Couldn't add {_role.name} from {member}.")
            return
        await ctx.reply(f"Successfully removed {_role.name} from {member}.")   
        
    @remove.error
    async def remerrh(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid member.")

    @role.command()
    async def info(self, ctx, role: discord.Role=None):
        """ Get information on a role. """
        if role is None:
            await ctx.reply("Please provide a role.")
            return
        created = role.created_at
        year = created.year
        month = created.month
        day = created.day
        p = role.permissions
        permissions = {"Administrator": p.administrator,
                       "Manage Guild": p.manage_guild,
                       "Manage Roles": p.manage_roles,
                       "Manage Channels": p.manage_channels,
                       "Kick Members": p.kick_members, 
                       "Ban members": p.ban_members, 
                       "Manage Nicknames": p.manage_nicknames,
                       "Manage Emojis": p.manage_emojis,
                       "Manage Webhooks": p.manage_webhooks,
                       "Mute Members": p.mute_members,
                       "Deafean Members": p.deafen_members,
                       "Move Members": p.move_members,
                       "Manage Messages": p.manage_messages,
                       "Mention Everyone": p.mention_everyone}
        msg = ''
        if not permissions["Administrator"]:
            for perm in permissions:
                a = permissions[perm]
                if a:
                    permissions[perm] = yes
                else:
                    permissions[perm] = no
                msg += f"{perm}: {permissions[perm]}\n"
        else: 
            msg += f"Administrator: {yes}"
        tech = {"Hoisted": role.hoist,
                "Managed": role.managed,
                "Mentionable": role.mention}
        msg2 = ''
        for t in tech:
            a = tech[t]
            if a:
                tech[t] = yes
            else:
                tech[t] = no
            msg2 += f"{t}: {tech[t]}\n"
        embed=discord.Embed(title=f"Information on role {role.name}", color=role.color)
        embed.add_field(name="General Information", value=f"Name: {role.name}\nId: {role.id}\nCreated: {month}/{day}/{year}", inline=True)   
        embed.add_field(name="Technical Stuff", value=msg2, inline=True)  
        embed.add_field(name="Key Permissions", value=msg, inline=True)
        await ctx.reply(embed=embed)

    @info.error
    async def infoerrh(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid role.")

    @role.command()
    async def create(self, ctx, name: str=None):
        """ Create a role. """
        if name is None:
            await ctx.reply("Please provide a role name.")
            return
        role = await ctx.guild.create_role(name=name, reason=f"Requested by {ctx.author}.")
        await ctx.reply(f"Successfully created {role.name}.")
        
    @role.command(aliases=['del'])
    async def delete(self, ctx, role: discord.Role=None):
        """ Delete a role. """
        if role is None:
            await ctx.reply("Please provide a role.")
            return
        await role.delete(reason=f"Deleted by {ctx.author}.")
        await ctx.reply(f"Successfully deleted {role.name}.")

    @delete.error
    async def delerrh(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid role.")

def setup(bot):
    bot.add_cog(Administration(bot))