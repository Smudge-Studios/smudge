import aiosqlite
from core.Exceptions import *

time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}

class AutoModSettingsManager:
    async def create(self, guild):
        i = True
        async with aiosqlite.connect('data\\automod.db') as conn:
            async with await conn.execute(f"SELECT * from CONFIG where GUILD = {guild}") as cursor:
                async for row in cursor:
                    if row[0] == guild:
                        i = False
                        break
            if i:
                await conn.execute(f"INSERT INTO CONFIG (GUILD) \
                    VALUES ({guild})")
            await conn.commit()

    async def settings(self, ctx):
        guild = ctx.guild
        config = dict({})
        spam = False
        links = False
        swear = False
        invites = False
        hoisting = False
        async with aiosqlite.connect('data\\automod.db') as conn:
            async with await conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}") as cursor:
                async for row in cursor:
                    if row[0] == guild.id:
                        spam = row[1]
                        links = row[2]
                        swear = row[3]
                        invites = row[4]
                        hoisting = row[5]
        config['spam'] = spam
        config['links'] = links
        config['swear'] = swear
        config['invites'] = invites
        config['hoisting'] = hoisting
        return config        
    
    async def antispam(self, ctx, setting):
        await self.create(ctx.guild.id)
        async with aiosqlite.connect('data\\automod.db') as conn:
            if setting:
                await conn.execute(f"UPDATE CONFIG set SPAM = True where GUILD = {ctx.guild.id}")
            else:
                await conn.execute(f"UPDATE CONFIG set SPAM = False where GUILD = {ctx.guild.id}")
            await conn.commit()

    async def antispamon(self, guildid):
        async with aiosqlite.connect('data\\automod.db') as conn:
            async with await conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}") as cursor:
                async for row in cursor:
                    if row[0] == guildid:
                        return row[1]

    async def antilinks(self, ctx, setting):
        guild = ctx.guild
        await self.create(ctx.guild.id)
        async with aiosqlite.connect('data\\automod.db') as conn:
            if setting:
                await conn.execute(f"UPDATE CONFIG set LINKS = True where GUILD = {guild.id}")
            else:
                await conn.execute(f"UPDATE CONFIG set LINKS = False where GUILD = {guild.id}")
            await conn.commit()

    async def antilinkson(self, guildid):
        async with aiosqlite.connect('data\\automod.db') as conn:
            async with await conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}") as cursor:
                async for row in cursor:
                    if row[0] == guildid:
                        return row[2]

    async def antiswear(self, ctx, setting):
        await self.create(ctx.guild.id)
        guild = ctx.guild
        async with aiosqlite.connect('data\\automod.db') as conn:
            if setting:
                await conn.execute(f"UPDATE CONFIG set SWEAR = True where GUILD = {guild.id}")
            else:
                await conn.execute(f"UPDATE CONFIG set SWEAR = False where GUILD = {guild.id}")
            await conn.commit()

    async def antiswearon(self, guildid):
        async with aiosqlite.connect('data\\automod.db') as conn:
            async with await conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}") as cursor:
                async for row in cursor:
                    if row[0] == guildid:
                        return row[3]

    async def antiinvites(self, ctx, setting):
        await self.create(ctx.guild.id)
        guild = ctx.guild
        async with aiosqlite.connect('data\\automod.db') as conn:
            if setting:
                await conn.execute(f"UPDATE CONFIG set INVITES = True where GUILD = {guild.id}")
            else:
                await conn.execute(f"UPDATE CONFIG set INVITES = False where GUILD = {guild.id}")
            await conn.commit()

    async def antiinviteson(self, guildid):
        async with aiosqlite.connect('data\\automod.db') as conn:
            async with await conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}") as cursor:
                async for row in cursor:
                    if row[0] == guildid:
                        return row[4]

    async def antihoist(self, ctx, setting):
        await self.create(ctx.guild.id)
        guild = ctx.guild
        async with aiosqlite.connect('data\\automod.db') as conn:
            if setting:
                await conn.execute(f"UPDATE CONFIG set HOISTING = True where GUILD = {guild.id}")
            else:
                await conn.execute(f"UPDATE CONFIG set HOISTING = False where GUILD = {guild.id}")
            await conn.commit()

    async def antihoiston(self, guildid):
        async with aiosqlite.connect('data\\automod.db') as conn:
            async with await conn.execute(f"SELECT * from CONFIG where GUILD = {guildid}") as cursor:
                async for row in cursor:
                    if row[0] == guildid:
                        return row[5]