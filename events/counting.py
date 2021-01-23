from core.UtilCore import *
import discord
from discord.ext import commands
import sqlite3
import asyncio

utils = Utils()

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            guild = message.guild
            if message.author.bot:
                return
            i = False
            async with aiosqlite.connect('data\\config.db') as conn:
                async with conn.execute("SELECT * from COUNTING") as cursor:
                    async for row in cursor:
                        if row[0] == guild.id:
                            if message.channel.id == row[1]:
                                i = row[2]+1
            if i is not False:
                try:
                    msg = int(message.content)
                except ValueError:
                    try:
                        await message.delete()
                    except discord.Forbidden:
                        return
                    except discord.NotFound:
                        return
                    return
                if msg == i:
                    await utils.count(guild.id, msg)
                else:
                    try:
                        await message.delete()
                    except discord.Forbidden:
                        return
                    except discord.NotFound:
                        return

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        i = False
        if isinstance(channel, discord.channel.TextChannel):
            async with aiosqlite.connect('data\\config.db') as conn:
                async with conn.execute("SELECT * from COUNTING") as cursor:
                    async for row in cursor:
                        if row[0] == channel.guild.id:
                            if channel.id == row[1]:
                                i = row[2]
        if i is not False:
            try:
                abcdefg = await channel.history(limit=1).flatten()
                recent = abcdefg[0]
                msg = await channel.fetch_message(payload.message_id)
                if msg.content == recent.content:
                    await msg.delete()
                    await channel.send(i)
            except discord.Forbidden:
                return
            except discord.NotFound:
                return

def setup(bot):
    bot.add_cog(Counting(bot))