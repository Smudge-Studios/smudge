print('Starting the Bot...')
import sqlite3
import discord
from discord.ext import commands
from configparser import ConfigParser
from core.UtilCore import Utils
from core.Pagination import Embeds
import random
import os

utils = Utils()
parser = ConfigParser()
parser.read('config.ini')
token = parser.get('CONFIG', 'token')
intents = discord.Intents.all()

class Help(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        embeds, paginator = await Embeds().Help().gen(self)
        if embeds is not None:
            await paginator.run(embeds, send_to=destination)

bot = commands.Bot(command_prefix = utils.get_prefix, case_insensitive=True, intents=intents, help_command=Help())

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

for file in os.listdir("automod"):
    if file.endswith(".py"):
        load_extension(f"automod.{file}".replace('.py',''))

for file in os.listdir("levels"):
    if file.endswith(".py"):
        load_extension(f"levels.{file}".replace('.py',''))

print(" Initializing databases...")
conn = sqlite3.connect('data/automod.db')
conn.execute("CREATE TABLE IF NOT EXISTS CONFIG ( \
            GUILD INT NOT NULL, \
            SPAM BOOLEAN NOT NULL DEFAULT FALSE, \
            LINKS BOOLEAN NOT NULL DEFAULT FALSE, \
            SWEAR BOOLEAN NOT NULL DEFAULT FALSE, \
            INVITES BOOLEAN NOT NULL DEFAULT FALSE, \
            HOISTING BOOLEAN NOT NULL DEFAULT FALSE \
            );")
conn.commit()
conn.close()
conn = sqlite3.connect('data/bot.db')
conn.execute("CREATE TABLE IF NOT EXISTS CONFIG ( \
            USER INT NOT NULL, \
            REASON TEXT NOT NULL DEFAULT NONE \
            );")
conn.commit()
conn.close()
conn = sqlite3.connect('data/config.db')
conn.execute("CREATE TABLE IF NOT EXISTS CONFIG ( \
            GUILD INT NOT NULL, \
            PREFIX TEXT NOT NULL DEFAULT '>', \
            SUGGESTIONS INT DEFAULT NONE, \
            REPORTS INT DEFAULT NONE, \
            MYSTBIN BOOLEAN NOT NULL DEFAULT NONE, \
            TOKENALERT BOOLEAN NOT NULL DEFAULT NONE, \
            LEVELS BOOLEAN NOT NULL DEFAULT NONE \
            );")
conn.execute("CREATE TABLE IF NOT EXISTS COUNTING ( \
            GUILD INT NOT NULL, \
            CHANNEL INT DEFAULT NONE, \
            NUMBER INT DEFAULT 0 \
            );")
conn.commit()
conn.close()
conn = sqlite3.connect('data/economy.db')
conn.execute("CREATE TABLE IF NOT EXISTS ECONOMY ( \
            USER INT NOT NULL, \
            WALLET INT NOT NULL DEFAULT 0, \
            BANK INT NOT NULL DEFAULT 200 \
            );")
conn.commit()
conn.close()
conn = sqlite3.connect('data/levels.db')
conn.execute("CREATE TABLE IF NOT EXISTS LEVELS ( \
            USER INT NOT NULL, \
            GUILD INT NOT NULL, \
            EXP INT NOT NULL DEFAULT 0, \
            MESSAGES INT NOT NULL DEFAULT 0 \
            );")
conn.execute("CREATE TABLE IF NOT EXISTS RANKS ( \
            GUILD INT NOT NULL, \
            LEVEL INT NOT NULL, \
            ROLE INT NOT NULL \
            );")
conn.commit()
conn.close()
conn = sqlite3.connect('data/moderation.db')
conn.execute("CREATE TABLE IF NOT EXISTS BANS ( \
            GUILD INT NOT NULL, \
            USER INT NOT NULL, \
            REASON TEXT NOT NULL DEFAULT 'None', \
            MOD INT NOT NULL, \
            ID INT NOT NULL, \
            EXPIRES INT NOT NULL DEFAULT -1, \
            EXPIRED BOOLEAN NOT NULL DEFAULT FALSE \
            );")
conn.execute("CREATE TABLE IF NOT EXISTS CONFIG ( \
            GUILD INT NOT NULL, \
            MUTEROLE INT NOT NULL \
            );")
conn.execute("CREATE TABLE IF NOT EXISTS KICKS ( \
            GUILD INT NOT NULL, \
            USER INT NOT NULL, \
            REASON TEXT NOT NULL DEFAULT 'None', \
            MOD INT NOT NULL, \
            ID INT NOT NULL \
            );")
conn.execute("CREATE TABLE IF NOT EXISTS MUTES ( \
            GUILD INT NOT NULL, \
            USER INT NOT NULL, \
            REASON TEXT NOT NULL DEFAULT 'None', \
            MOD INT NOT NULL, \
            ID INT NOT NULL, \
            EXPIRES INT NOT NULL DEFAULT -1, \
            EXPIRED BOOLEAN NOT NULL DEFAULT FALSE \
            );")
conn.execute("CREATE TABLE IF NOT EXISTS PUNISHMENTS ( \
            WARNS INT NOT NULL DEFAULT 0, \
            MUTES INT NOT NULL DEFAULT 0, \
            KICKS TEXT NOT NULL DEFAULT 0, \
            BANS INT NOT NULL DEFAULT 0, \
            TOTAL INT NOT NULL DEFAULT 0 \
            );")
conn.execute("INSERT INTO PUNISHMENTS (WARNS, MUTES, KICKS, BANS, TOTAL) \
    VALUES (0, 0, 0, 0, 0)")
conn.execute("CREATE TABLE IF NOT EXISTS WARNS ( \
            GUILD INT NOT NULL, \
            USER INT NOT NULL, \
            REASON TEXT NOT NULL DEFAULT 'None', \
            MOD INT NOT NULL, \
            ID INT NOT NULL \
            );")
conn.commit()
conn.close()


print(' Logging In...')
try:
    bot.run(token)
except Exception as e:
    print(' ' + str(e))
