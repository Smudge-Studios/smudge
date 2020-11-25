import discord
from discord.ext import tasks, commands
from core.ModCore import Mod

mod = Mod()

class AutoUnban(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.unban.start()

    def cog_unload(self):
        self.unban.cancel()

    @tasks.loop(seconds=60.0)
    async def unban(self):
        guilds, members = mod.autounban()
        i = 0
        for g in guilds:
            y = True
            try:
                guild = self.bot.get_guild(g)
                user = guild.get_member(members[i])
                try:
                    member = discord.Object(id=int(user))
                    await guild.unban(member, reason=f"Automatic unban.")
                except:
                    y = False
                i=i+1
                if y == True:
                    try:
                        await user.send(f"You have been automatically unbanned in {guild.name}.")
                    except discord.HTTPException:
                        pass
            except:
                pass

    @unban.before_loop
    async def before_unban(self):
        print('Waiting to run AutoUnban task...')
        await self.bot.wait_until_ready()
        print('Running AutoUnban...')

def setup(bot):
    bot.add_cog(AutoUnban(bot))