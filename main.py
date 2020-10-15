print('Starting bot...')
print(' Importing Modules...')
import discord
from discord.ext import commands
print(' Modules imported.')



def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['s!','S!']


    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix = get_prefix, case_insensitive=True)
bot.remove_command('help')
TOKEN = 'NzY0Njc3ODMzODIwOTk1NjA1.X4Jvug.kugM9cHroOi6sHecHqc4uMdTEAw'

initial_extensions = ['events.ready',
                      'events.commanderror']

print(' Loading Cogs...')
if __name__ == '__main__':
    for extension in initial_extensions:
        print("     Loading extension " + extension + '...')
        bot.load_extension(extension)
        print('     Extension ' + extension + ' loaded.')
print(' Cogs loaded.')



print(' Logging In...')
try:
    bot.run(TOKEN, bot=True, reconnect=True)
except Exception as e:
    print(' ' + str(e))
