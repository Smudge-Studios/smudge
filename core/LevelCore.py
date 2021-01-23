import random
import aiosqlite
from core.Exceptions import *

class Levels:
    async def level(self, xp):
        level = 0
        beforexp = 0
        nxt_lvl_xp = 0
        for lvl in range(1, 1000):
            lvl_xp = 5 / 6 * lvl * (2 * lvl * lvl + 27 * lvl + 91)
            xp_needed = lvl_xp - xp
            level = lvl-1
            if xp_needed >= 0:
                lvl_xp = 5 / 6 * lvl * (2 * lvl * lvl + 27 * lvl + 91)
                exp = 5 / 6 * (lvl-1) * (2 * (lvl-1) * (lvl-1) + 27 * (lvl-1) + 91)
                beforexp = exp+1
                nxt_lvl_xp = lvl_xp+1
                break
        return level, int(beforexp), int(nxt_lvl_xp)
        
    async def addexp(self, member, guild, amnt):
        i = True
        if not member.bot:
            async with aiosqlite.connect('data\\levels.db') as conn:
                async with conn.execute(f"SELECT * from LEVELS where USER = {member.id} and GUILD = {guild}") as cursor:
                    async for row in cursor:
                        if row[0] == member.id:
                            if row[1] == member.guild.id:
                                level, i, z = await self.level(row[2])
                                a = amnt + row[2]
                                msgs = row[3]+1
                                await conn.execute(f"UPDATE LEVELS set EXP = {a}, MESSAGES = {msgs} where GUILD = {guild} and USER = {member.id}")
                                await conn.commit()
                                level2, i, z = await self.level(a)
                                if level2 > level:
                                    return level2
                                i = False
                                return -1
                if i:
                    await conn.execute(f"INSERT INTO LEVELS (USER, GUILD, EXP, MESSAGES) \
                        VALUES ({member.id}, {guild}, {amnt}, 1)")
                    await conn.commit()
                    return -1
            
    async def remexp(self, member, guild, amnt):
        i = True
        if not member.bot:
            async with aiosqlite.connect('data\\levels.db') as conn:
                async with conn.execute(f"SELECT * from LEVELS where USER = {member.id} and GUILD = {guild}") as cursor:
                    async for row in cursor:
                        if row[0] == member.id:
                            if row[1] == member.guild.id:
                                level, i, z = await self.level(row[2])
                                a = row[2] - amnt
                                if a < 0:
                                    raise ValueError("Cannot remove more XP than the user has.")
                                await conn.execute(f"UPDATE LEVELS set EXP = {a} where GUILD = {guild} and USER = {member.id}")
                                await conn.commit()
                                level2, i, z = await self.level(a)
                                if level2 < level:
                                    return level2
                                i = False
                                return -1
                if i:
                    await conn.execute(f"INSERT INTO LEVELS (USER, GUILD, EXP, MESSAGES) \
                        VALUES ({member.id}, {guild}, 0, 0)")
                    await conn.commit()
                    raise ValueError("Cannot remove more XP than the user has.")

    async def leaders(self, guild):
        lvls = []
        lvldict = dict({})
        async with aiosqlite.connect('data\\levels.db') as conn:
            async with conn.execute(f"SELECT * from LEVELS where GUILD = {guild}") as cursor:
                async for row in cursor:
                    if row[1] == guild:
                        if row[2] > 0:
                            level, req_xp, nxt_lvl_xp = await self.level(row[2])
                            del(req_xp)
                            del(nxt_lvl_xp)
                            if level not in lvls:
                                lvls.append(level)
                            if level in lvldict:
                                if isinstance(lvldict[level], list):
                                    l = lvldict[level]
                                    lvldict[level] = []
                                    lvldict[level].extend(l)
                                    lvldict[level].append(row[0])
                                else:
                                    user = lvldict[level]
                                    lvldict[level] = []
                                    lvldict[level].append(user)
                                    lvldict[level].append(row[0])
                            else:
                                lvldict[level] = row[0]
        return lvls, lvldict

    async def insert(self, user, guild):
        i = True
        async with aiosqlite.connect('data\\levels.db') as conn:
            async with conn.execute(f"SELECT * from LEVELS where GUILD = {guild} and USER = {user}") as cursor:
                async for row in cursor:
                    if row[0] == user:
                        if row[1] == guild:
                            i = False
            if i:
                await conn.execute(f"INSERT INTO LEVELS (USER, GUILD) \
                    VALUES ({user}, {guild})")
                await conn.commit()

    async def fetchrank(self, user, guild):
        async with aiosqlite.connect('data\\levels.db') as conn:
            async with conn.execute(f"SELECT * from LEVELS where GUILD = {guild} and USER = {user}") as cursor:
                async for row in cursor:
                    if row[0] == user:
                        if row[1] == guild:
                            xp = row[2]
                            level, before_xp, nxt_lvl_xp = await self.level(xp)
                            exp = int(xp-before_xp+1)
                            e = '['
                            percent = int((exp/nxt_lvl_xp)*10)
                            for i in range(percent):
                                e += '='
                            a = 10-percent
                            for i in range(a):
                                e += '⠀'
                            e += f'] {exp}/{nxt_lvl_xp} XP'
                            xp = row[2]
                            msgs = row[3]
                            return level, xp, e, msgs
            await self.insert(user, guild)
            level = 0
            xp = 0
            msgs = 0
            e = '[⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀] 0/101 XP'
            return level, xp, e, msgs

    async def addrank(self, guild, role, level):
        i = True
        async with aiosqlite.connect('data\\levels.db') as conn:
            async with conn.execute(f"SELECT * from RANKS where GUILD = {guild} and LEVEL = {level}") as cursor:
                async for row in cursor:
                    if row[0] == guild:
                        if row[1] == level:
                            i = False
            if i:
                await conn.execute(f"INSERT INTO RANKS (GUILD, LEVEL, ROLE) \
                    VALUES ({guild}, {level}, {role})")
                await conn.commit()
                return("added")
            if not i:
                await conn.execute(f"UPDATE RANKS set ROLE = {role} where GUILD = {guild} and LEVEL = {level}")
                await conn.commit()
                return("updated")

    async def deleterank(self, guild, level):
        i = True
        async with aiosqlite.connect('data\\levels.db') as conn:
            async with conn.execute(f"SELECT * from RANKS where GUILD = {guild} and LEVEL = {level}") as cursor:
                async for row in cursor:
                    if row[0] == guild:
                        if row[1] == level:
                            i = False
            if i:
                raise ValueError
            if not i:
                await conn.execute(f"DELETE from RANKS where GUILD = {guild} and LEVEL = {level}")
                await conn.commit()
                return("deleted")

    async def getranks(self, guild):
        diction = dict({})
        async with aiosqlite.connect('data\\levels.db') as conn:
            async with conn.execute(f"SELECT * from RANKS where GUILD = {guild}") as cursor:
                async for row in cursor:
                    if row[0] == guild:
                        diction[row[1]] = row[2]
        return diction


