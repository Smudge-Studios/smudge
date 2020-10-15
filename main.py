print('Starting bot...')
print(' Importing Modules...')
import discord
from discord.ext import commands
print(' Modules imported.')



def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    prefixes = ['s!','S!']


    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix = get_prefix, case_insensitive=True)
bot.remove_command('help')
TOKEN = 'NzY2MTU3NDcxMjY5Mzg4MzU5.X4fRvw.CJIj7VYZTOzwI7_0pgWoo8Ul-4k'

initial_extensions = ['events.ready',
                      'events.commanderror',
                      'events.memberjoin',
                      'commands.owner.load',
                      'commands.owner.unload',
                      'commands.owner.reload',
                      'commands.help']

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
