print('Starting the Bot...')
print(' Importing Modules...')
import sqlite3
import discord
from discord.ext import commands
from configparser import ConfigParser
from core.UtilCore import Utils
import random
print(' Modules imported.')

print(' Defining constants...')
utils = Utils()
parser = ConfigParser()
parser.read('config.ini')
token = parser.get('CONFIG', 'token')
conn = sqlite3.connect('data\\config.db')
intents = discord.Intents.default()
intents.members = True
print(' Constants defined.')

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        color=random.randint(1, 16777215)
        e = discord.Embed(title="Help", color=color, description='')
        pages = -1
        p = 0
        for page in self.paginator.pages:
            pages = pages+1
        e.description += f"`Page {p+1}/{pages+1}`\n\n"
        e.description += self.paginator.pages[p]
        await destination.send(embed=e)

bot = commands.Bot(command_prefix = utils.get_prefix, case_insensitive=True, intents=intents, help_command=MyHelpCommand())

initial_extensions = ['commands.admins',
                      'commands.eco',
                      'commands.fun',
                      'commands.moderation',
                      'commands.owner',
                      'commands.util',
                      'events.botjoin',
                      'events.counting',
                      'events.error',
                      'events.ready',
                      'events.userjoin',
                      'tasks.bans',
                      'tasks.mutes']

print(' Loading Cogs...')
if __name__ == '__main__':
    for extension in initial_extensions:
        print("     Loading extension " + extension + '...')
        try:
            bot.load_extension(extension)
            print('     Extension ' + extension + ' loaded.')
        except Exception as e:
            print(f"     {e}")
print(' Cogs loaded.')

print(' Logging In...')
try:
    bot.run(token)
except Exception as e:
    print(' ' + str(e))
