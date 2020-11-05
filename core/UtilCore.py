from core.Exceptions import *
import sqlite3

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