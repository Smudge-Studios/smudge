import discord
from discord.ext import tasks, commands
import time
import sqlite3

conn = sqlite3.connect('data\\moderation.db')

class AutoUnban(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.unban.start()

    def cog_unload(self):
        self.unban.cancel()

    @tasks.loop(seconds=60.0)
    async def unban(self):
        cursor = conn.execute("SELECT * from BANS")
        now = int(time.time())
        try:
            for row in cursor:
                if row[5] <= now:
                    if row[6] == True:
                        return
                    conn.execute(f"UPDATE BANS set EXPIRED = TRUE where USER = {row[1]}")
                    conn.commit()
                    guild = self.bot.get_guild(row[0])
                    if guild == None:
                        return
                    user = guild.get_member(row[1])
                    if user == None:
                        return
                    try:
                        await guild.unban(user, reason="Automatic unban.")
                    except discord.Forbidden:
                        pass
                    try:
                        await user.send(f"You have been automatically unbanned in {guild.name}.")
                    except discord.Forbidden:
                        pass
        except Exception as e:
            print(f"Couldn't check unbans: {e}")

    @unban.before_loop
    async def before_unban(self):
        print('Waiting to run AutoUnban task...')
        await self.bot.wait_until_ready()
        print('Running AutoUnban...')

def setup(bot):
    bot.add_cog(AutoUnban(bot))