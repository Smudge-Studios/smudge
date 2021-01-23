from core.Exceptions import *
import aiosqlite
import time
from core.AutoModSettings import AutoModSettingsManager
from core.LevelCore import Levels
from discord.ext import commands

levels = Levels()

class Utils:
    async def reportchannel(self, ctx):
        guild = ctx.guild
        async with aiosqlite.connect('data\\config.db') as conn:
            async with conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}") as cursor:
                async for row in cursor:
                    if row[0] == guild.id:
                        if row[3] is None:
                            raise error.Unable("This guild does not have a report channel set.")
                        channel = guild.get_channel(row[3])
                        if channel == None:
                            raise error.Unable("This guild does not have a report channel set.")
                        return channel
        raise error.Unable("This guild does not have a report channel set.")

    async def setreportchannel(self, ctx, channel):
        guild = ctx.guild
        async with aiosqlite.connect('data\\config.db') as conn:
            if channel == 'remove':
                await conn.execute(f"UPDATE CONFIG set REPORTS = Null where GUILD = {guild.id}")
            else:
                async with conn.execute(f"SELECT * from CONFIG where GUILD = {ctx.guild.id}") as cursor:
                    cr = True
                    async for row in cursor:
                        if row[0] == ctx.guild.id:
                            conn.execute(f"UPDATE CONFIG set REPORTS = {channel.id} where GUILD = {guild.id}")
                            cr = False
                            break
                    if cr:
                        conn.execute(f"INSERT INTO CONFIG (GUILD,PREFIX,REPORTS) \
                            VALUES ({ctx.guild.id}, '>', {channel.id})")
            await conn.commit()

    async def suggestchannel(self, ctx):
        guild = ctx.guild
        async with aiosqlite.connect('data\\config.db') as conn:
            async with conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}") as cursor:
                async for row in cursor:
                    if row[0] == guild.id:
                        if row[2] is None:
                            raise error.Unable("This guild does not have a suggestion channel set.")
                        channel = guild.get_channel(row[2])
                        if channel == None:
                            raise error.Unable("This guild does not have a suggestion channel set.")
                        return channel
        raise error.Unable("This guild does not have a suggestion channel set.")

    async def setsuggestionchannel(self, ctx, channel):
        guild = ctx.guild
        async with aiosqlite.connect('data\\config.db') as conn:
            if channel == 'remove':
                await conn.execute(f"UPDATE CONFIG set SUGGESTIONS = Null where GUILD = {guild.id}")
            else:
                async with conn.execute("SELECT * from CONFIG") as cursor:
                    cr = True
                    for row in cursor:
                        if row[0] == ctx.guild.id:
                            await conn.execute(f"UPDATE CONFIG set SUGGESTIONS = {channel.id} where GUILD = {guild.id}")
                            cr = False
                            break
                    if cr:
                        await conn.execute(f"INSERT INTO CONFIG (GUILD,PREFIX,SUGGESTIONS) \
                            VALUES ({ctx.guild.id}, '>', {channel.id})")
            await conn.commit()

    async def setcountingchannel(self, ctx, channel):
        guild = ctx.guild
        async with aiosqlite.connect('data\\config.db') as conn:
            if channel == 'remove':
                await conn.execute(f"UPDATE COUNTING set CHANNEL = Null where GUILD = {guild.id}")
            else:
                async with conn.execute("SELECT * from COUNTING") as cursor:
                    cr = True
                    async for row in cursor:
                        if row[0] == ctx.guild.id:
                            await conn.execute(f"UPDATE COUNTING set CHANNEL = {channel.id} where GUILD = {guild.id}")
                            cr = False
                            break
                    if cr:
                        await conn.execute(f"INSERT INTO COUNTING (GUILD,CHANNEL,NUMBER) \
                            VALUES ({ctx.guild.id}, {channel.id}, 0)")
            await conn.commit()

    async def count(self, guild, msg):
        async with aiosqlite.connect('data\\config.db') as conn:
            await conn.execute(f"UPDATE COUNTING set NUMBER = {int(msg)} where GUILD = {int(guild)}")
            await conn.commit()

    async def setprefix(self, ctx, prefix):
        guild = ctx.guild.id
        async with aiosqlite.connect('data\\config.db') as conn:
            await conn.execute(f"UPDATE CONFIG set PREFIX = ? where GUILD = {guild}", (f'{prefix}'))
            await conn.commit()

    async def get_prefix(self, bot, message):
        """A callable Prefix for our bot. This could be edited to allow per server prefixes."""
        async with aiosqlite.connect('data\\config.db') as conn:
            async with conn.execute("SELECT * from CONFIG") as cursor:
                async for row in cursor:
                    if row[0] == message.guild.id:
                        await levels.insert(message.author.id, message.author.guild.id)
                        prefixes = [row[1]]
                        return commands.when_mentioned_or(*prefixes)(bot, message)
            await conn.execute(f"INSERT INTO COUNTING (GUILD) \
                VALUES ({message.guild.id})")
            await conn.execute(f"INSERT INTO CONFIG (GUILD, PREFIX) \
                VALUES ({message.guild.id}, '>')")
        await AutoModSettingsManager().create(message.guild.id)
        await levels.insert(message.author.id, message.author.guild.id)
        prefixes = ['>']
        return commands.when_mentioned_or(*prefixes)(bot, message)
    
    async def get_readable_prefix(self, ctx):
        guild = ctx.guild
        async with aiosqlite.connect('data\\config.db') as conn:
            async with conn.execute("SELECT * from CONFIG") as cursor:
                async for row in cursor:
                    if row[0] == guild.id:
                        levels.insert(ctx.author.id, guild.id)
                        return row[1]
            await conn.execute(f"INSERT INTO COUNTING (GUILD) \
                VALUES ({ctx.guild.id})")
            await conn.execute(f"INSERT INTO CONFIG (GUILD, PREFIX) \
                VALUES ({ctx.guild.id}, '>')")
        await AutoModSettingsManager().create(ctx.guild.id)
        await levels.insert(ctx.author.id, ctx.author.guild.id)
        return '>'

    async def poll(self, input):
        options = input.split('|')
        question = options[0]
        options.remove(question)
        for a in options:
            if a == '':
                options.remove(a)
        if len(options) > 5:
            raise error.Unable("Sorry, you may only use 5 answers.")
        elif len(options) <= 1:
            raise error.Unable("Please specify more than one option.")
        return question, options

    async def get_config(self, ctx):
        guild = ctx.guild
        prefix = '>'
        countchannel = None
        suggestionchannel = None
        reportschannel = None
        mistbin = False
        tokenalert = False
        levels = False
        config = dict({})
        async with aiosqlite.connect('data\\config.db') as conn:
            async with conn.execute(f"SELECT * from COUNTING where GUILD = {guild.id}") as cursor:
                async for row in cursor:
                    if row[0] == guild.id:
                        countchannel = row[1]
            async with conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}") as cursor:
                async for row in cursor:
                    if row[0] == guild.id:
                        prefix = row[1]
                        suggestionchannel = row[2]
                        reportschannel = row[3]
                        mistbin = row[4]
                        tokenalert = row[5]
                        levels = row[6]
        config['counting'] = countchannel
        config['prefix'] = prefix
        config['suggestions'] = suggestionchannel
        config['reports'] = reportschannel
        config['mistbin'] = mistbin
        config['token'] = tokenalert
        config['levels'] = levels
        return config        

    async def mistbin(self, ctx, setting):
        guild = ctx.guild
        async with aiosqlite.connect('data\\config.db') as conn:
            if setting:
                await conn.execute(f"UPDATE CONFIG set MYSTBIN = True where GUILD = {guild.id}")
            else:
                await conn.execute(f"UPDATE CONFIG set MYSTBIN = False where GUILD = {guild.id}")
            await conn.commit()

    async def tokenalerter(self, ctx, setting):
        guild = ctx.guild
        async with aiosqlite.connect('data\\config.db') as conn:
            if setting:
                await conn.execute(f"UPDATE CONFIG set TOKENALERT = True where GUILD = {guild.id}")
            else:
                await conn.execute(f"UPDATE CONFIG set TOKENALERT = False where GUILD = {guild.id}")
            await conn.commit()

    async def tokenon(self, guildid):
        async with aiosqlite.connect('data\\config.db') as conn:
            async with conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}") as cursor:
                async for row in cursor:
                    if row[0] == guildid:
                        return row[5]

    async def mistbinon(self, guildid):
        async with aiosqlite.connect('data\\config.db') as conn:
            async with conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}") as cursor:
                async for row in cursor:
                    if row[0] == guildid:
                        return row[4]

    async def levels(self, ctx, setting):
        guild = ctx.guild
        async with aiosqlite.connect('data\\config.db') as conn:
            if setting:
                await conn.execute(f"UPDATE CONFIG set LEVELS = True where GUILD = {guild.id}")
            else:
                await conn.execute(f"UPDATE CONFIG set LEVELS = False where GUILD = {guild.id}")
            await conn.commit()

    async def levelson(self, guildid):
        async with aiosqlite.connect('data\\config.db') as conn:
            async with conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}") as cursor:
                async for row in cursor:
                    if row[0] == guildid:
                        return row[6]

