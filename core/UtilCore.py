from core.Exceptions import *
import sqlite3
import time

conn = sqlite3.connect('data\\config.db')

class Utils:
    def reportchannel(self, ctx):
        guild = ctx.guild
        cursor = conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}")
        for row in cursor:
            if row[0] == guild.id:
                if row[3] is None:
                    raise error.Unable("This guild does not have a report channel set.")
                channel = guild.get_channel(row[3])
                if channel == None:
                    raise error.Unable("This guild does not have a report channel set.")
                return channel

    def setreportchannel(self, ctx, channel):
        guild = ctx.guild
        if channel == 'remove':
            conn.execute(f"UPDATE CONFIG set REPORTS = Null where GUILD = {guild.id}")
        else:
            cursor = conn.execute("SELECT * from CONFIG")
            try:
                cr = True
                for row in cursor:
                    if row[0] == ctx.guild.id:
                        conn.execute(f"UPDATE CONFIG set REPORTS = {channel.id} where GUILD = {guild.id}")
                        cr = False
                        break
                if cr==True:
                    raise ValueError
            except ValueError:
                conn.execute(f"INSERT INTO CONFIG (GUILD,PREFIX,REPORTS) \
                    VALUES ({ctx.guild.id}, '>', {channel.id})")
        conn.commit()

    def suggestchannel(self, ctx):
        guild = ctx.guild
        cursor = conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}")
        for row in cursor:
            if row[0] == guild.id:
                if row[2] is None:
                    raise error.Unable("This guild does not have a suggestion channel set.")
                channel = guild.get_channel(row[2])
                if channel == None:
                    raise error.Unable("This guild does not have a suggestion channel set.")
                return channel

    def setsuggestionchannel(self, ctx, channel):
        guild = ctx.guild
        if channel == 'remove':
            conn.execute(f"UPDATE CONFIG set SUGGESTIONS = Null where GUILD = {guild.id}")
        else:
            cursor = conn.execute("SELECT * from CONFIG")
            try:
                cr = True
                for row in cursor:
                    if row[0] == ctx.guild.id:
                        conn.execute(f"UPDATE CONFIG set SUGGESTIONS = {channel.id} where GUILD = {guild.id}")
                        cr = False
                        break
                if cr==True:
                    raise ValueError
            except ValueError:
                conn.execute(f"INSERT INTO CONFIG (GUILD,PREFIX,SUGGESTIONS) \
                    VALUES ({ctx.guild.id}, '>', {channel.id})")
        conn.commit()

    def setcountingchannel(self, ctx, channel):
        guild = ctx.guild
        if channel == 'remove':
            conn.execute(f"UPDATE COUNTING set CHANNEL = Null where GUILD = {guild.id}")
        else:
            cursor = conn.execute("SELECT * from COUNTING")
            try:
                cr = True
                for row in cursor:
                    if row[0] == ctx.guild.id:
                        conn.execute(f"UPDATE COUNTING set CHANNEL = {channel.id} where GUILD = {guild.id}")
                        cr = False
                        break
                if cr==True:
                    raise ValueError
            except ValueError:
                conn.execute(f"INSERT INTO COUNTING (GUILD,CHANNEL,NUMBER) \
                    VALUES ({ctx.guild.id}, {channel.id}, 0)")
        conn.commit()

    def count(self, guild, msg):
        conn.execute(f"UPDATE COUNTING set NUMBER = {int(msg)} where GUILD = {int(guild.id)}")
        conn.commit()

    def setprefix(self, ctx, prefix):
        guild = ctx.guild.id
        conn.execute(f"UPDATE CONFIG set PREFIX = '{prefix}' where GUILD = {guild}")
        conn.commit()

    def get_prefix(self, bot, message):
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
            return(">")

    def poll(self, input):
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

    def get_config(self, ctx):
        guild = ctx.guild
        cursor = conn.execute(f"SELECT * from COUNTING where GUILD = {guild.id}")
        cursor2 = conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}")
        prefix = '>'
        countchannel = None
        suggestionchannel = None
        reportschannel = None
        mistbin = False
        tokenalert = False
        config = dict({})
        for row in cursor:
            if row[0] == guild.id:
                countchannel = row[1]
        for row in cursor2:
            if row[0] == guild.id:
                prefix = row[1]
                suggestionchannel = row[2]
                reportschannel = row[3]
                mistbin = row[4]
                tokenalert = row[5]
        config['counting'] = countchannel
        config['prefix'] = prefix
        config['suggestions'] = suggestionchannel
        config['reports'] = reportschannel
        config['mistbin'] = mistbin
        config['token'] = tokenalert
        return config        

    def mistbin(self, ctx, setting):
        guild = ctx.guild
        if setting:
            conn.execute(f"UPDATE CONFIG set MYSTBIN = True where GUILD = {guild.id}")
        else:
            conn.execute(f"UPDATE CONFIG set MYSTBIN = False where GUILD = {guild.id}")
        conn.commit()

    def tokenalerter(self, ctx, setting):
        guild = ctx.guild
        if setting:
            conn.execute(f"UPDATE CONFIG set TOKENALERT = True where GUILD = {guild.id}")
        else:
            conn.execute(f"UPDATE CONFIG set TOKENALERT = False where GUILD = {guild.id}")
        conn.commit()

    def tokenon(self, guildid):
        cursor = conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}")
        for row in cursor:
            if row[0] == guildid:
                return row[5]

    def mistbinon(self, guildid):
        cursor = conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}")
        for row in cursor:
            if row[0] == guildid:
                return row[4]