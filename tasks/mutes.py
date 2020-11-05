import discord
from discord.ext import tasks, commands
import time
import sqlite3

conn = sqlite3.connect('data\\moderation.db')

class AutoUnmute(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.unmute.start()

    def cog_unload(self):
        self.unmute.cancel()

    @tasks.loop(seconds=60.0)
    async def unmute(self):
        cursor = conn.execute("SELECT * from MUTES")
        now = int(time.time())
        try:
            for row in cursor:
                if row[5] <= now:
                    if row[6] == True:
                        return
                    conn.execute(f"UPDATE MUTES set EXPIRED = TRUE where USER = {row[1]}")
                    conn.commit()
                    guild = self.bot.get_guild(row[0])
                    if guild == None:
                        return
                    user = guild.get_member(row[1])
                    if user == None:
                        return
                    try:
                        cursor2 = conn.execute("SELECT * from CONFIG")
                        for row in cursor2:
                            if row[0] == guild.id:
                                muterole = guild.ret_role(row[1])
                        user.remove_roles(muterole)
                    except discord.Forbidden:
                        pass
                    try:
                        await user.send(f"You have been automatically unmuted in {guild.name}.")
                    except discord.Forbidden:
                        pass
        except Exception as e:
            print(f"Couldn't check unmutes: {e}")

    @unmute.before_loop
    async def before_unmute(self):
        print('Waiting to run AutoUnmute task...')
        await self.bot.wait_until_ready()
        print('Running AutoUnmute...')

def setup(bot):
    bot.add_cog(AutoUnmute(bot))