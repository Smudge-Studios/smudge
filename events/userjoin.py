import discord
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('data\\moderation.db')

class UserJoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cursor = conn.execute("SELECT * from MUTES")
        guild = member.guild
        for row in cursor:
            if row[1] == member.id:
                if row[0] == guild.id:
                    if row[6] != True:
                        cursor2 = conn.execute("SELECT * from CONFIG")
                        for row in cursor2:
                            if row[0] == guild.id:
                                muterole = guild.get_role(row[1])
                        try:
                            await member.add_role(muterole)
                            try:
                                await member.send(f"You were automatically muted in {guild.name}, as you have an unexpired mute in that server.")
                            except discord.Forbidden:
                                pass
                        except discord.Forbidden:
                            pass
                        

def setup(bot):
    bot.add_cog(UserJoin(bot))