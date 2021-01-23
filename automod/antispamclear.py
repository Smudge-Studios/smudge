import discord
from discord.ext import tasks, commands

class ClearAntispamfile(commands.Cog):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.ClearAntispamfile.start()

    def cog_unload(self):
        self.ClearAntispamfile.cancel()

    @tasks.loop(seconds=3)
    async def ClearAntispamfile(self):
        with open("automod\\messages.txt", 'w') as file:
            file.write("")

    @ClearAntispamfile.before_loop
    async def before_ClearAntispamfile(self):
        print('Waiting to run ClearAntispamfile task...')
        await self.bot.wait_until_ready()
        print('Running ClearAntispamfile...')

def setup(bot):
    bot.add_cog(ClearAntispamfile(bot))