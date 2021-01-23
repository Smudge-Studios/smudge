import discord
from discord.ext import tasks, commands

class ClearLevelfile(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.ClearLevelfile.start()

    def cog_unload(self):
        self.ClearLevelfile.cancel()

    @tasks.loop(minutes=1)
    async def ClearLevelfile(self):
        with open("levels\\messages.txt", 'w') as file:
            file.write("")

    @ClearLevelfile.before_loop
    async def before_ClearAntispamfile(self):
        print('Waiting to run ClearLevelfile task...')
        await self.bot.wait_until_ready()
        print('Running ClearLevelfile...')

def setup(bot):
    bot.add_cog(ClearLevelfile(bot))