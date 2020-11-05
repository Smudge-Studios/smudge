import discord
from discord.ext import commands
import sys
import traceback

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return
        
        # If a user tries to run a nonexistant command
        if isinstance(error, commands.CommandNotFound):
            return

        # If the bot doesn't have enough permissions
        if isinstance(error, commands.BotMissingPermissions):
            perms = ', '.join(error.missing_perms)
            await ctx.send(f"Sorry, I require the permissions `{perms}` to execute that command.")

        # If a user doesn't provide a required argument
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Error", description="""Missing Required Argument.""", color=0xff0000)
            await ctx.send(embed=embed)
            return
        
        # If a user tries to run a restricted command
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Error", description="""This command is restricted.""", color=0xff0000)
            await ctx.send(embed=embed)
            return

        # If a user provides an invalid argument
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Invalid argument. Please try again.')
            return

        #If discord throws an HTTP error
        elif isinstance(error, discord.HTTPException):
            print("Discord HTTP Exception: " + str(error))
            return

        # If the user is blacklisted
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'You are blacklisted from my economy. Reason: {error}')
            return
        
        # If the command is on a cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            timeout = str(error.retry_after)
            timeout = timeout.replace('s','')
            seconds = int(float(timeout))
            min, sec = divmod(seconds, 60) 
            hour, min = divmod(min, 60) 
            if hour == 0:
                if min == 0:
                    if sec == 1:
                        await ctx.send(f"That command is on cooldown. You may try again in {sec} second.")
                    else:
                        await ctx.send(f"That command is on cooldown. You may try again in {sec} seconds.")
                elif min == 1:
                    await ctx.send(f"That command is on cooldown. You may try again in {min} minute.")
                else:
                    await ctx.send(f"That command is on cooldown. You may try again in {min} minutes.")
            elif hour == 1:
                await ctx.send(f"That command is on cooldown. You may try again in {hour} hour.")
            else:
                await ctx.send(f"That command is on cooldown. You may try again in {hour} hours.")
            return

        # If the user provides an argument that has quotes and the bot gets pissed off
        elif isinstance(error, commands.InvalidEndOfQuotedStringError) or isinstance(error, commands.ExpectedClosingQuoteError) or isinstance(error, commands.UnexpectedQuoteError):
            await ctx.send('Invalid argument. Please omit any quotes in the command.')
            return

        # If the user doesnt have enough permissions to run a command
        elif isinstance(error, commands.MissingPermissions):
            perms = ', '.join(error.missing_perms)
            await ctx.send(f'Sorry, you need the permission `{perms}` to execute this command.')
            return

        # If the error is not recognized
        else:
            embed = discord.Embed(title="Error", description="""An unknown error occurred. This error has been reported.
            `""" + str(error) + '`', color=0xff0000)
            await ctx.send(embed=embed)
            print("")
            print('Ignoring exception in command {}.'.format(ctx.command), file=sys.stderr)
            print("=====(BEGIN ERROR OUTPUT)=====")
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            print("=====(END ERROR OUTPUT)=====")
            return

def setup(bot):
    bot.add_cog(ErrorHandler(bot))