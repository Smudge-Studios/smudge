import discord
from discord.ext import commands
import asyncio
import requests
        
class OnJoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        #channel = general channel id
        embed = discord.Embed(title="Welcome", description=f"Please welcome <@{member}> to the server!", color=0x00ff00)
        await channel.send(embed=embed)
        try:
            embed = discord.Embed(title="Welcome", description=f"Hello <@{member}>, welcome to Smudge Studios! Please ensure that you read the rules in the <#ruleschannelid>, and have fun!", color=0x00ff00)
            await member.send(embed=embed)
        except:
            return

def setup(bot):
    bot.add_cog(OnJoin(bot))