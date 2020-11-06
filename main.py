print('Starting the Bot...')
print(' Importing Modules...')
import sqlite3
import discord
from discord.ext import commands
from configparser import ConfigParser
print(' Modules imported.')

print(' Defining constants...')
parser = ConfigParser()
parser.read('config.ini')
token = parser.get('CONFIG', 'token')
conn = sqlite3.connect('data\\config.db')
intents = discord.Intents.all()
intents.members = True
print(' Constants defined.')

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
    cursor = conn.execute("SELECT * from CONFIG")
    for row in cursor:
        if row[0] == message.guild.id:
            return row[1]
    else:
        conn.execute(f"INSERT INTO COUNTING (GUILD) \
            VALUES ({message.guild.id})")
        conn.execute(f"INSERT INTO CONFIG (GUILD, PREFIX) \
            VALUES ({message.guild.id}, '>')")

bot = commands.Bot(command_prefix = get_prefix, case_insensitive=True, intents=intents)
bot.remove_command('help')

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
