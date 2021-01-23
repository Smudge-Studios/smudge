import random
import aiosqlite
from core.Exceptions import *

class Data:
    async def create(self, user):
        """ Adds a new user to the database. """
        async with aiosqlite.connect('data\\economy.db') as conn:
            await conn.execute(f"INSERT INTO ECONOMY (USER,WALLET,BANK) \
                VALUES ({user}, 0, 200)")
            await conn.commit()

    async def check(self, user):
        """ Checks if a user is in the database.
            If not, it adds them to the database."""
        async with aiosqlite.connect('data\\economy.db') as conn:
            async with conn.execute("SELECT * from ECONOMY") as cursor:
                async for row in cursor:
                    if row[0] == user:
                        return
        await self.create(user)
    
    async def delete(self, user):
        try:
            async with aiosqlite.connect('data\\economy.db') as conn:
                await conn.execute(f"DELETE from ECONOMY where USER = {user}")
                await conn.commit()
        except aiosqlite.OperationalError as e:
            if str(e) == f'no such column: {user}':
                raise ValueError
            else:
                raise e

data = Data()

class Wallet:
    async def get(self, user):
        """ Gets the balance of somebody's wallet. """
        await data.check(user)
        async with aiosqlite.connect('data\\economy.db') as conn:
            async with conn.execute("SELECT * from ECONOMY") as cursor:
                async for row in cursor:
                    if row[0] == user:
                        return row[1]

    async def add(self, user, add):
        """ Adds money to somebody's wallet. """
        await data.check(user)
        async with aiosqlite.connect('data\\economy.db') as conn:
            async with conn.execute("SELECT * from ECONOMY") as cursor:
                bal = 0
                async for row in cursor:
                    if row[0] == user:
                        bal = row[1] + add
            await conn.execute(f"UPDATE ECONOMY set WALLET = {bal} where USER = {user}")
            await conn.commit()

    async def remove(self, user, take):
        """ Removes money from somebody's wallet. """
        await data.check(user)
        async with aiosqlite.connect('data\\economy.db') as conn:
            async with conn.execute("SELECT * from ECONOMY") as cursor:
                bal = 0
                async for row in cursor:
                    if row[0] == user:
                        bal = row[1] - take
            await conn.execute(f"UPDATE ECONOMY set WALLET = {bal} where USER = {user}")
            await conn.commit()

class Bank:
    async def get(self, user):
        """ Get someone's bank balance. """
        await data.check(user)
        async with aiosqlite.connect('data\\economy.db') as conn:
            async with conn.execute("SELECT * from ECONOMY") as cursor:
                async for row in cursor:
                    if row[0] == user:
                        return row[2]

    async def add(self, user, add):
        """ Adds money to someone's bank. """
        await data.check(user)
        async with aiosqlite.connect('data\\economy.db') as conn:
            async with conn.execute("SELECT * from ECONOMY") as cursor:
                bal = 0
                async for row in cursor:
                    if row[0] == user:
                        bal = row[2] + add
            await conn.execute(f"UPDATE ECONOMY set BANK = {bal} where USER = {user}")
            await conn.commit()

    async def remove(self, user, take):
        """ Removes money from someone's bank. """
        await data.check(user)
        async with aiosqlite.connect('data\\economy.db') as conn:
            async with conn.execute("SELECT * from ECONOMY") as cursor:
                bal = 0
                async for row in cursor:
                    if row[0] == user:
                        bal = row[2] - take
                        print(bal)
            await conn.execute(f"UPDATE ECONOMY set BANK = {bal} where USER = {user}")
            await conn.commit()

wallet = Wallet()
bank = Bank()

class Eco:
    async def deposit(self, user, amount):
        """ Deposits money from somebody's wallet to their bank. """
        bal = await wallet.get(user)
        if bal < amount:
            raise error.NEMU
        elif bal == 0:
            raise error.FAIL
        await wallet.remove(user, amount)
        await bank.add(user, amount)

    async def withdraw(self, user, amount):
        """ Withdraws money from somebody's bank to their wallet. """
        bal = await bank.get(user)
        if bal < amount:
            raise error.NEMU
        elif bal == 0:
            raise error.FAIL
        await bank.remove(user, amount)
        await wallet.add(user, amount)

    async def rob(self, user, target):
        """ Robs 1/5 of the money in somebody's wallet with a 20% chance of success and gives it the the theif. 
            If robbery fails, theif pays target $200. """
        targetw = await wallet.get(target)
        if targetw < 500:
            raise error.NEMT
        elif targetw < 200:
            raise error.NEMU
        if random.randint(1, 100) <= 20:
            amount = targetw(target)/5
            await wallet.remove(target, amount)
            await wallet.add(user, amount)
            return amount
        else:
            await wallet.remove(user, 200)
            await wallet.add(target, 200)
            raise error.FAIL

    async def pay(self, user, target, amount):
        """ Allows people to transfer currency between themselves. """
        if await wallet.get(user) < amount:
            raise error.NEMU
        await wallet.add(target, amount)
        await wallet.remove(user, amount)

eco = Eco()