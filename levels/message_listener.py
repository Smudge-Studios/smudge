import discord
from discord.ext import commands
from core.LevelCore import Levels
from core.UtilCore import Utils
import random

levels = Levels()
utils = Utils()

class LevelListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message is not None:
            try:
                if message.author.guild is not None:
                    if await utils.levelson(message.guild.id):
                        with open("levels\\messages.txt", 'r') as file:
                            content = file.read()
                        if f"{message.author.id}:{message.guild.id}" not in content:
                            amnt = random.randint(15, 25)
                            i = await levels.addexp(message.author, message.guild.id, amnt)
                            with open("levels\\messages.txt", 'a') as file:
                                file.writelines(f"{str(message.author.id)}:{str(message.guild.id)}\n")
                            if i != -1:
                                ranks = await levels.getranks(message.guild.id)
                                for r in ranks:
                                    if r < i:
                                        role = message.guild.get_role(ranks[r])
                                        if role is not None:
                                            try:
                                                await message.author.add_roles(role)
                                            except:
                                                pass
                                await message.channel.send(f"Congratulations {message.author.mention}, you have leveled up to level {i}!")
            except AttributeError:
                pass


def setup(bot):
    bot.add_cog(LevelListener(bot))
