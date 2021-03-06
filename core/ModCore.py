import aiosqlite
from core.Exceptions import *
import time

time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}

async def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

class Mod:
    async def gettime(self, time1):
        if time1 is None:
            return None
        return int(time1[:-1]) * time_convert[time1[-1]]

    async def ban(self, ctx, member, reason, duration):
        guild = ctx.guild
        num = 0
        total = 0
        async with aiosqlite.connect('data\\moderation.db') as conn:
            async with conn.execute("SELECT * from BANS") as cursor:
                async for row in cursor:
                    if row[2] == member.id:
                        if row[6] == 0:
                            mod = guild.get_member(row[3])
                            raise error.Unable(f"That user is already banned. Moderator: {mod.name}. Reason: {row[2]}")
            async with conn.execute(f"SELECT * from PUNISHMENTS") as cursor:
                async for row in cursor:
                    num = row[3]+1
                    total = row[4]+1
            await conn.execute(f"UPDATE PUNISHMENTS set BANS = {num}")
            await conn.execute(f"UPDATE PUNISHMENTS set TOTAL = {total}")
            await conn.execute(f"INSERT INTO BANS (GUILD,USER,REASON,MOD,ID,EXPIRES,EXPIRED) \
                        VALUES ('{guild.id}', '{member.id}', ?, '{ctx.author.id}', '{total}', '{duration}', FALSE)", (reason,))
            await conn.commit()
        return True

    async def kick(self, ctx, member, reason):
        guild = ctx.guild
        num = 0
        total = 0
        async with aiosqlite.connect('data\\moderation.db') as conn:
            async with conn.execute(f"SELECT * from PUNISHMENTS") as cursor:
                async for row in cursor:
                    num = row[2]+1
                    total = row[4]+1
            await conn.execute(f"UPDATE PUNISHMENTS set KICKS = {num}")
            await conn.execute(f"UPDATE PUNISHMENTS set TOTAL = {total}")
            await conn.execute(f"INSERT INTO KICKS (GUILD,USER,REASON,MOD,ID) \
                        VALUES ('{guild.id}', '{member.id}', ?, '{ctx.author.id}', '{total}')", (reason,))
            await conn.commit()
        return True
    
    async def mute(self, ctx, member, reason, duration):
        guild = ctx.guild
        muterole = None
        async with aiosqlite.connect('data\\moderation.db') as conn:
            async with conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}") as cursor:
                async for row in cursor:
                    if row[0] == ctx.guild.id:
                        muterole = row[1]
                        break
            muterole = guild.get_role(muterole)
            if muterole is None:
                raise error.Unable(f"This server doesn't have a muterole. Please set one with the `muterole` command.")
            if muterole in member.roles:
                raise error.Unable(f"{member.name} is already muted.")
            num = 0
            total = 0
            async with conn.execute(f"SELECT * from PUNISHMENTS") as cursor:
                async for row in cursor:
                    num = row[1]+1
                    total = row[4]+1
            await conn.execute(f"UPDATE PUNISHMENTS set MUTES = {num}")
            await conn.execute(f"UPDATE PUNISHMENTS set TOTAL = {total}")
            await conn.execute(f"INSERT INTO MUTES (GUILD, USER, REASON, MOD, ID, EXPIRES, EXPIRED) \
                    VALUES ('{guild.id}', '{member.id}', ?, '{ctx.author.id}', '{total}', '{duration}', False)", (reason,))
            await conn.commit()
        return muterole

    async def warn(self, ctx, member, mod, reason):
        guild = ctx.guild
        num = 0
        total = 0
        async with aiosqlite.connect('data\\moderation.db') as conn:
            async with conn.execute(f"SELECT * from PUNISHMENTS") as cursor:
                async for row in cursor:
                    num = row[0]+1
                    total = row[4]+1
            await conn.execute(f"UPDATE PUNISHMENTS set WARNS = {num}")
            await conn.execute(f"UPDATE PUNISHMENTS set TOTAL = {total}")
            await conn.execute(f"INSERT INTO WARNS (GUILD, USER, REASON, MOD, ID) \
                    VALUES ('{guild.id}', '{member.id}', '{reason}', '{mod.id}', '{total}')")
            await conn.commit()
            warns = 0
            async with conn.execute(f"SELECT * from WARNS where USER = {member.id} and GUILD = {guild.id}") as cursor:
                async for row in cursor:
                    if row[0] == guild.id:
                        if row[1] == member.id:
                            warns = warns+1
        return ord(warns)

    async def unban(self, ctx, member):
        guild = ctx.guild
        async with aiosqlite.connect('data\\moderation.db') as conn:
            await conn.execute(f"UPDATE BANS set EXPIRED = TRUE where USER = {member.id} and GUILD = {guild.id}")
            await conn.commit()
        return True

    async def autounban(self):
        now = int(time.time())
        guilds = []
        members = []
        async with aiosqlite.connect('data\\moderation.db') as conn:
            async with conn.execute("SELECT * from BANS") as cursor:
                async for row in cursor:
                    if row[5] != -1:
                        if row[5] <= now:
                            if row[6] is not True:
                                await conn.execute(f"UPDATE BANS set EXPIRED = TRUE where USER = {row[1]}")
                                await conn.commit()
                                guild = row[0]
                                member = row[1]
                                guilds.append(guild)
                                members.append(member)
        return guilds, members

    async def unmute(self, ctx, member):
        guild = ctx.guild
        muterole = None
        async with aiosqlite.connect('data\\moderation.db') as conn:
            async with conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}") as cursor:
                async for row in cursor:
                    if row[0] == ctx.guild.id:
                        muterole = row[1]
                        break
            if muterole is None:
                raise error.Unable(f"This server does not have a muterole set.")
            muterole = guild.get_role(muterole)
            if muterole not in member.roles:
                raise error.Unable(f"{member.name} is not muted.")
            await conn.execute(f"UPDATE MUTES set EXPIRED = TRUE where USER = {member.id} and GUILD = {guild.id}")
            await conn.commit()
        return muterole

    async def autounmute(self):
        now = int(time.time())
        guildsl = []
        membersl = []
        rolesl = []
        async with aiosqlite.connect('data\\moderation.db') as conn:
            async with conn.execute("SELECT * from MUTES") as cursor:
                async for row in cursor:
                    if row[5] != -1:
                        if row[5] <= now:
                            if row[6] is not True:
                                conn.execute(f"UPDATE MUTES set EXPIRED = TRUE where USER = {row[1]}")
                                cursor2 = conn.execute("SELECT * from CONFIG")
                                guild = row[0]
                                member = row[1]
                                muterole = None
                                for row in cursor2:
                                    if row[0] == guild:
                                        muterole = row[1]
                                        break
                                guildsl.append(guild)
                                membersl.append(member)
                                rolesl.append(muterole)
        return guildsl, membersl, rolesl
                        
    async def fetchpunishlist(self, ctx, member, type):
        guild = ctx.guild
        p = ["BANS", "WARNS", "MUTES", "KICKS"]
        ids = []
        reasons = []
        types = []
        if type is not None:
            if type.upper() not in p:
                raise error.Unable("Invalid punishment types.\nPlease choose either `bans`, `kicks`, `mutes` or `warns`.")
            type = type.upper()
        elif type is None:
            async with aiosqlite.connect('data\\moderation.db') as conn:
                for i in p:
                    async with conn.execute(f"SELECT * from {i} where GUILD = {guild.id} and USER = {member.id}") as cursor:
                        async for row in cursor:
                            if row[0] == ctx.guild.id:
                                if row[1] == member.id:
                                    reasons.append(row[2])
                                    ids.append(row[4])
                                    types.append(i)
                if len(ids) == 0:
                    raise error.Unable(f"{member.name} has no punishments.")
                return ids, reasons, types
        async with aiosqlite.connect('data\\moderation.db') as conn:
            async with conn.execute(f"SELECT * from {type} where GUILD = {guild.id} and USER = {member.id}") as cursor:
                async for row in cursor:
                    if row[0] == ctx.guild.id:
                        if row[1] == member.id:
                            reasons.append(row[2])
                            ids.append(row[4])
                            types.append(type)
        return ids, reasons, types               

    async def fetchpunish(self, ctx, id):
        guild = ctx.guild
        p = ["BANS", "WARNS", "MUTES", "KICKS"]
        async with aiosqlite.connect('data\\moderation.db') as conn:
            for i in p:
                async with conn.execute(f"SELECT * from {i} where ID = {id} and GUILD = {guild.id}") as cursor:
                    async for row in cursor:
                        if row[4] == id:
                            if row[0] == guild.id:
                                return row, i
        raise error.Unable(f"Couldn't find a punishment with the ID {id}.")

    async def delpunish(self, ctx, id):
        guild = ctx.guild
        p = ["BANS", "WARNS", "MUTES", "KICKS"]
        for i in p:
            async with aiosqlite.connect('data\\moderation.db') as conn:
                async with conn.execute(f"SELECT * from {i} where ID = {id}") as cursor:
                    async for row in cursor:
                        if row[4] == id:
                            if row[0] == guild.id:
                                await conn.execute(f"DELETE from {i} where ID = {id} and GUILD = {guild.id}")
                                await conn.commit()
                                return
        raise error.Unable(f"Couldn't find a punishment with the ID {id}.")