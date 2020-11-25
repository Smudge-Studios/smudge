import discord
from discord.ext import tasks, commands
from core.ModCore import Mod

mod = Mod()

class AutoUnmute(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.unmute.start()

    def cog_unload(self):
        self.unmute.cancel()

    @tasks.loop(seconds=60.0)
    async def unmute(self):
        guilds, members, roles = mod.autounmute()
        i = 0
        for g in guilds:
            y = True
            try:
                guild = self.bot.get_guild(g)
                user = guild.get_member(members[i])
                muterole = guild.get_role(roles[i])
                try:
                    await user.remove_roles(muterole)
                except:
                    y = False
                i=i+1
                if y == True:
                    try:
                        await user.send(f"You have been automatically unmuted in {guild.name}.")
                    except discord.HTTPException:
                        pass
            except:
                pass

    @unmute.before_loop
    async def before_unmute(self):
        print('Waiting to run AutoUnmute task...')
        await self.bot.wait_until_ready()
        print('Running AutoUnmute...')

def setup(bot):
    bot.add_cog(AutoUnmute(bot))