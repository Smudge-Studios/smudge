from configparser import ConfigParser
import shutil
import random
import sqlite3
from core.Exceptions import *

conn = sqlite3.connect('data\\economy.db')

class data:
    def read(self):
        """ Reads the database. """
        return conn.execute("SELECT * from ECONOMY")

    def save(self):
        """ Saves all changed data to the database. """
        conn.commit()

data = data()


class file:
    def create(self, user):
        """ Adds a new user to the database. """
        conn.execute(f"INSERT INTO ECONOMY (USER,WALLET,BANK) \
            VALUES ({user}, 350, 200)")

file = file()

class file2:
    def check(self, user):
        """ Checks if a user is in the database.
            If not, it adds them to the database."""
        cursor = data.read()
        for row in cursor:
            if row[0] == user:
                return
        file.create(user)
    
    def delete(self, user):
        try:
            conn.execute(f"DELETE from ECONOMY where USER = {user}")
            data.save()
        except sqlite3.OperationalError as e:
            if str(e) == f'no such column: {user}':
                raise ValueError
            else:
                raise e


file2 = file2()

class wallet:
    def get(self, user):
        """ Gets the balance of somebody's wallet. """
        file2.check(user)
        cursor = data.read()
        for row in cursor:
            if row[0] == user:
                return row[1]

    def add(self, user, add):
        """ Adds money to somebody's wallet. """
        file2.check(user)
        cursor = data.read()
        bal = 0
        for row in cursor:
            if row[0] == user:
                bal = row[1] + add
        conn.execute(f"UPDATE ECONOMY set WALLET = {bal} where USER = {user}")
        data.save()

    def remove(self, user, take):
        """ Removes money from somebody's wallet. """
        file2.check(user)
        cursor = data.read()
        bal = 0
        for row in cursor:
            if row[0] == user:
                bal = row[1] - take
        conn.execute(f"UPDATE ECONOMY set WALLET = {bal} where USER = {user}")
        data.save()

class bank:
    def get(self, user):
        """ Get someone's bank balance. """
        file2.check(user)
        cursor = data.read()
        for row in cursor:
            if row[0] == user:
                return row[2]

    def add(self, user, add):
        """ Adds money to someone's bank. """
        file2.check(user)
        cursor = data.read()
        bal = 0
        for row in cursor:
            if row[0] == user:
                bal = row[2] + add
        conn.execute(f"UPDATE ECONOMY set BANK = {bal} where USER = {user}")
        data.save()

    def remove(self, user, take):
        """ Removes money from someone's bank. """
        file2.check(user)
        cursor = data.read()
        bal = 0
        for row in cursor:
            if row[0] == user:
                bal = row[2] - take
                print(bal)
        conn.execute(f"UPDATE ECONOMY set BANK = {bal} where USER = {user}")
        data.save()
        pass

wallet = wallet()
bank = bank()

class Eco:
    def deposit(self, user, amount):
        """ Deposits money from somebody's wallet to their bank. """
        bal = wallet.get(user)

        if bal < amount:
            raise error.NEMU
        elif bal == 0:
            raise error.FAIL
        wallet.remove(user, amount)
        bank.add(user, amount)

    def withdraw(self, user, amount):
        """ Withdraws money from somebody's bank to their wallet. """
        bal = bank.get(user)
        if bal < amount:
            raise error.NEMU
        elif bal == 0:
            raise error.FAIL
        bank.remove(user, amount)
        wallet.add(user, amount)

    def rob(self, user, target):
        """ Robs 1/5 of the money in somebody's wallet with a 20% chance of success and gives it the the theif. 
            If robbery fails, theif pays target $200. """
        if wallet.get(target) < 500:
            raise error.NEMT
        elif wallet.get(user) < 200:
            raise error.NEMU
        if random.randint(1, 100) <= 20:
            amount = wallet.get(target)/5
            wallet.remove(target, amount)
            wallet.add(user, amount)
            return amount
        else:
            wallet.remove(user, 200)
            wallet.add(target, 200)
            raise error.FAIL

    def pay(self, user, target, amount):
        """ Allows people to transfer currency between themselves. """
        if wallet.get(user) < amount:
            raise error.NEMU
        wallet.add(target, amount)
        wallet.remove(user, amount)

eco = Eco()