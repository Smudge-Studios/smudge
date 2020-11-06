import sqlite3
import asyncio
from core.Exceptions import *

loop = asyncio.get_event_loop()
time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
conn = sqlite3.connect('data\\moderation.db')

def thstndrd(number):
    return str(number)+("th" if 4<=number%100<=20 else {1:"st",2:"nd",3:"rd"}.get(number%10, "th"))

class Mod:
    def gettime(self, time):
        return int(time[:-1]) * time_convert[time[-1]]

    def ban(self, ctx, member, reason, duration):
        guild = ctx.guild
        mempos = member.top_role.position
        me = guild.get_member(self.bot.user.id)
        mepos = me.top_role.position
        if mempos >= mepos:
            raise error.Unable(f"Unable to ban {member.name} due to role hierarchy.")
        elif guild.owner == member:
            raise error.Unable(f"I cannot ban the guild's owner.")
        cursor = conn.execute("SELECT * from BANS")
        for row in cursor:
            if row[2] == member.id:
                if row[6] == 0:
                    mod = guild.get_member(row[3])
                    raise error.Unable(f"That user is already banned. Moderator: {mod.name}. Reason: {row[2]}")
        cursor = conn.execute(f"SELECT * from PUNISHMENTS")
        for row in cursor:
            num = row[3]+1
            total = row[4]+1
        conn.execute(f"UPDATE PUNISHMENTS set BANS = {num}")
        conn.execute(f"UPDATE PUNISHMENTS set TOTAL = {total}")
        conn.execute(f"INSERT INTO BANS (GUILD,USER,REASON,MOD,ID,EXPIRES,EXPIRED) \
                    VALUES ({guild.id}, {member.id}, {reason}, {ctx.author.id}, {total}, {duration}, FALSE)")
        conn.commit()
        return True

    def kick(self, ctx, member, reason):
        guild = ctx.guild
        mempos = member.top_role.position
        me = guild.get_member(self.bot.user.id)
        mepos = me.top_role.position
        if mempos >= mepos:
            raise error.Unable(f"Unable to kick {member.name} due to role hierarchy.")
        elif guild.owner == member:
            raise error.Unable(f"I cannot kick the guild's owner.")
        cursor = conn.execute(f"SELECT * from PUNISHMENTS")
        for row in cursor:
            num = row[2]+1
            total = row[4]+1
        conn.execute(f"UPDATE PUNISHMENTS set KICKS = {num}")
        conn.execute(f"UPDATE PUNISHMENTS set TOTAL = {total}")
        conn.execute(f"INSERT INTO KICKS (GUILD,USER,REASON,MOD,ID) \
                    VALUES ({guild.id}, {member.id}, {reason}, {ctx.author.id}, {total})")
        conn.commit()
        return True
    
    def mute(self, ctx, member, reason, duration):
        guild = ctx.guild
        mempos = member.top_role.position
        me = guild.get_member(self.bot.user.id)
        mepos = me.top_role.position
        if mempos >= mepos:
            raise error.Unable(f"Unable to mute {member.name} due to role hierarchy.")
        elif guild.owner == member:
            raise error.Unable(f"I cannot mute the guild's owner.")
        cursor = conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}")
        muterole = None
        for row in cursor:
            if row[0] == ctx.guild.id:
                muterole = row[1]
                break
        if muterole is None:
            raise error.Unable(f"This server doesn't have a muterole. Please set one with the `muterole` command.")
        muterole = guild.get_role(muterole)
        if muterole in member.roles:
            raise error.Unable(f"{member.name} is already muted.")
        cursor = conn.execute(f"SELECT * from PUNISHMENTS")
        for row in cursor:
            num = row[1]+1
            total = row[4]+1
        conn.execute(f"UPDATE PUNISHMENTS set MUTES = {num}")
        conn.execute(f"UPDATE PUNISHMENTS set TOTAL = {total}")
        conn.execute(f"INSERT INTO MUTES (GUILD,USER,REASON,MOD,ID,EXPIRES,EXPIRED) \
                    VALUES ({guild.id}, {member.id}, {reason}, {ctx.author.id}, {total}, {duration}, FALSE)")
        conn.commit()
        return muterole

    def warn(self, ctx, member, reason):
        guild = ctx.guild
        mempos = member.top_role.position
        me = guild.get_member(self.bot.user.id)
        mepos = me.top_role.position
        if mempos >= mepos:
            raise error.Unable(f"Unable to warn {member.name} due to role hierarchy.")
        elif guild.owner == member:
            raise error.Unable(f"I cannot warn the guild's owner.")
        cursor = conn.execute(f"SELECT * from PUNISHMENTS")
        for row in cursor:
            num = row[0]+1
            total = row[4]+1
        conn.execute(f"UPDATE PUNISHMENTS set WARNS = {num}")
        conn.execute(f"UPDATE PUNISHMENTS set TOTAL = {total}")
        conn.execute(f"INSERT INTO WARNS (GUILD,USER,REASON,MOD,ID) \
                    VALUES ({guild.id}, {member.id}, {reason}, {ctx.author.id}, {total})")
        conn.commit()
        cursor = conn.execute(f"SELECT * from WARNS where USER = {member.id} and GUILD = {guild.id}")
        warns = 0
        for row in cursor:
            if row[0] == guild.id:
                if row[1] == member.id:
                    warns = warns+1
        return ord(warns)

    def unban(self, ctx, member):
        guild = ctx.guild
        conn.execute(f"UPDATE BANS set EXPIRED = TRUE where USER = {member.id} and GUILD = {guild.id}")
        conn.commit()
        return True

    def unmute(self, ctx, member):
        guild = ctx.guild
        muterole = None
        cursor = conn.execute(f"SELECT * from CONFIG where GUILD = {guild.id}")
        for row in cursor:
            if row[0] == ctx.guild.id:
                muterole = row[1]
                break
        if muterole is None:
            raise error.Unable(f"{member.name} is not muted.")
        muterole = guild.get_role(muterole)
        if muterole not in member.roles:
            raise error.Unable(f"{member.name} is not muted.")
        conn.execute(f"UPDATE MUTES set EXPIRED = TRUE where USER = {member.id} and GUILD = {guild.id}")
        conn.commit()
        return muterole

    def fetchpunishlist(self, ctx, member, type):
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
            for i in p:
                cursor = conn.execute(f"SELECT * from {i} where GUILD = {guild.id} and USER = {member.id}")
                for row in cursor:
                    if row[0] == ctx.guild.id:
                        if row[1] == member.id:
                            reasons = reasons.append(row[2])
                            ids = ids.append(row[4])
                            types = types.append(i)
            if len(ids) == 0:
                raise error.Unable(f"{member.name} has no punishments.")
            return ids, reasons, types
        cursor = conn.execute(f"SELECT * from {type} where GUILD = {guild.id} and USER = {member.id}")
        for row in cursor:
            if row[0] == ctx.guild.id:
                if row[1] == member.id:
                    reasons = reasons.append(row[2])
                    ids = ids.append(row[4])
                    types = types.append(type)
        return ids, reasons, types               

    def fetchpunish(self, ctx, id):
        guild = ctx.guild
        p = ["BANS", "WARNS", "MUTES", "KICKS"]
        for i in p:
            cursor = conn.execute(f"SELECT * from {i} where ID = {id} and GUILD = {guild.id}")
            for row in cursor:
                if row[4] == id:
                    if row[0] == guild.id:
                        return row, i
        raise error.Unable(f"Couldn't find a punishment with the ID {id}.")

    def delpunish(self, ctx, id):
        guild = ctx.guild
        p = ["BANS", "WARNS", "MUTES", "KICKS"]
        for i in p:
            cursor = conn.execute(f"SELECT * from {i} where ID = {id}")
            for row in cursor:
                if row[4] == id:
                    if row[0] == guild.id:
                        conn.execute(f"DELETE from {i} where ID = {id} and GUILD = {guild.id}")
                        return
        raise error.Unable(f"Couldn't find a punishment with the ID {id}.")