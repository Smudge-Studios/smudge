print('Starting the Bot...')
import sqlite3
import discord
from discord.ext import commands
from configparser import ConfigParser
from core.UtilCore import Utils
import random
import os

utils = Utils()
parser = ConfigParser()
parser.read('config.ini')
token = parser.get('CONFIG', 'token')
conn = sqlite3.connect('data\\config.db')
intents = discord.Intents.default()
intents.members = True

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        color=random.randint(1, 16777215)
        e = discord.Embed(title="Help", color=color, description='')
        for page in self.paginator.pages:
            e.description += f"{page}\n"
        await destination.send(embed=e)

bot = commands.Bot(command_prefix = utils.get_prefix, case_insensitive=True, intents=intents, help_command=MyHelpCommand())

initial_extensions = ['commands.admins',
                      'commands.eco',
                      'commands.fun',
                      'commands.moderation',
                      'commands.owner',
                      'commands.util',
                      'commands.help',
                      'events.botjoin',
                      'events.counting',
                      'events.error',
                      'events.ready',
                      'events.mistbin',
                      'events.userjoin',
                      'events.tokens',
                      'tasks.bans',
                      'tasks.mutes']

def load_extension(extension):
    try:
        bot.load_extension(extension)
        print(f"{extension} loaded.")
    except Exception as e:
        print(f"Couldn't load {extension}: {e}")

for file in os.listdir("commands"):
    if file.endswith(".py"):
        load_extension(f"commands.{file}".replace('.py',''))

for file in os.listdir("events"):
    if file.endswith(".py"):
        load_extension(f"events.{file}".replace('.py',''))

for file in os.listdir("tasks"):
    if file.endswith(".py"):
        load_extension(f"tasks.{file}".replace('.py',''))

print(' Logging In...')
try:
    bot.run(token)
except Exception as e:
    print(' ' + str(e))
