import discord
from discord.ext import commands
import random
from core.EcoCore import *
import aiosqlite

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Cog check. Checks if blacklisted user invoked cog."""
        async with aiosqlite.connect('data\\bot.db') as conn:
            async with conn.execute("SELECT * from BLACKLIST") as cursor:
                async for row in cursor:
                    if row[0] == ctx.author.id:
                        await ctx.reply(f"You are blacklisted from my economy. Reason: {row[1]}")
                        raise commands.DisabledCommand
        return True

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def beg(self, ctx):
        """ Beg for money. """
        possibilities = [50, 25, 25, 30]
        add = random.choice(possibilities)
        await wallet.add(ctx.author.id, add)
        messages = [f'You begged on the streets and Elon Musk gave you ${add}.',
                    f'You stood outside of Walmart for an hour and someone gave you ${add}',
                    f'You stood outside a homeless shelter and earned ${add}']
        message = random.choice(messages)
        await ctx.reply(message)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member=None):
        """ Check somebody's balance, or your own if member isn't specified. """
        if member is None:
            user = ctx.author.name
            userid = ctx.author.id
        else:
            if member.bot:
                await ctx.reply("Can't check the balance of a bot.")
                return
            user = member.name
            userid = member.id
        color=random.randint(1, 16777215)
        embed = discord.Embed(title=f"{user}'s Balance", color=color)
        embed.add_field(name='Wallet', value=f'${await wallet.get(userid)}')
        embed.add_field(name='Bank', value=f'${await bank.get(userid)}')
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @balance.error
    async def ehidk(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """ Claim your daily reward. """
        user = ctx.author.id
        await wallet.add(user, 500)
        color=random.randint(1, 16777215)
        embed = discord.Embed(title=f"Daily Reward", description='You collected your daily reward! $500 was added to your wallet.', color=color)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amnt):
        """ Deposit money from your wallet to your bank. """
        user = ctx.author.id
        bal = await wallet.get(user)
        color=random.randint(1, 16777215)
        if not amnt:
            embed = discord.Embed(title=f"Deposit", description='Please specify an amount.', color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        try:
            if amnt.lower() == 'all':
                amnt = bal
        except:
            pass
        else:
            try:
                amnt = int(amnt)
            except ValueError:
                embed = discord.Embed(title=f"Deposit", description='Please specify a valid number.', color=0xff0000)
                embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return
        try:
            await eco.deposit(user, amnt)
            embed = discord.Embed(title=f"Deposit", description=f'Successfully deposited `${amnt}`.', color=color)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
        except error.NEMU:
            embed = discord.Embed(title=f"Deposit", description=f'Insufficient funds.', color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
        except error.FAIL:
            await ctx.reply("Nothing to deposit.")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amnt):
        """ Withdraw money from your bank to your wallet. """
        user = ctx.author.id
        bal = await bank.get(user)
        color=random.randint(1, 16777215)
        if not amnt:
            embed = discord.Embed(title=f"Withdraw", description='Please specify an amount.', color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        try:
            if amnt.lower() == 'all':
                amnt = bal
        except:
            pass
        else:
            try:
                amnt = int(amnt)
            except ValueError:
                embed = discord.Embed(title=f"Withdraw", description='Please specify a valid number.', color=0xff0000)
                embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return
        try:
            eco.withdraw(user, amnt)
            embed = discord.Embed(title=f"Withdraw", description=f'Successfully withdrew `${amnt}`.', color=color)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
        except error.NEMU:
            embed = discord.Embed(title=f"Withdraw", description=f'Insufficient funds.', color=0xff0000)
            embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
        except error.FAIL:
            await ctx.reply("Nothing to withdraw.")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member=None):
        """ Attempt to rob from someone's wallet. """
        robcmd = self.rob
        if member is None:
            await ctx.reply('Please specify a user to rob from.')
            robcmd.reset_cooldown(ctx)
            return
        try:
            if member.bot:
                await ctx.reply("You can't rob a bot.")
                robcmd.reset_cooldown(ctx)
                return
            amount_robbed = await eco.rob(ctx.author.id, member.id)
            await ctx.reply(f"You got into {member.name}'s wallet and got away with ${amount_robbed}.")
        except error.NEMT:
            await ctx.reply("That person doesn't have more than $500, it aint worth it man.")
            robcmd.reset_cooldown(ctx)
        except error.NEMU:
            await ctx.reply("You need at least $200 in your wallet to rob someone.")
            robcmd.reset_cooldown(ctx)
        except error.FAIL:
            await ctx.reply(f"You got caught in the act, and was forced to pay `{member.name}` a fine of $200.")

    @rob.error
    async def ehidk1(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command()
    async def pay(self, ctx, member: discord.Member=None, amount: str=None):
        """ Pay someone some money. """
        if member is None:
            await ctx.reply("Please specify someone to send money to.")
            return
        if amount is None:
            await ctx.reply("Please specify the amount of money you want to send.")
            return
        if member.bot:
            await ctx.reply("You can't pay a bot.")
            return
        try:
            amount = int(amount)
        except ValueError:
            await ctx.reply("Invalid amount.")
            return
        try:
            await eco.pay(ctx.author.id, member.id, amount)
            await ctx.reply(f"Successfully sent `${amount}` to `{member.name}`.")
        except error.NEMU:
            await ctx.reply(f"You do not have enough money to send `${amount}` to `{member.name}`.")

    @pay.error
    async def ehidk2(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Please provide an actual member.")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        """ Do some work and get paid for it. """
        possibilities = [50, 50, 100, 150]
        add = random.choice(possibilities)
        await wallet.add(ctx.author.id, add)
        messages = [f'You worked as a Discord Bot developer and earned ${add}.',
                    f"You fixed McDonald's Soft Serve machine and they gave you ${add}.",
                    f'You made YouTube videos and earned ${add} from ad revenue.']
        message = random.choice(messages)
        await ctx.reply(message)


def setup(bot):
    bot.add_cog(Economy(bot))