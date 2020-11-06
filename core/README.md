# Core
'Documentation' for bot cores.

This really isn't meant for use anywhere but this bot, as it's pretty much 100% hard coded.

ToDo: Exceptions, ModCore, UtilCore

# Quick Links
[EcoCore](https://github.com/Smudge-Studios/smudge/tree/main/core#ecocore)

[Exceptions]()

[ModCore]()

[UtilCore]()

# EcoCore
A core that can be imported as a module for Smudge's economy.

## class data
Literally just reads the database and commits changes.
### read()
Reads everything in the ECONOMY table in `economy.db`.
### save()
Commits all changes to the database.



## class file
The first `file` class
### create(user)
Creates a new entry in the database.


## class file2
The second `file` class
### check(user)
Checks if a user is in the database. If not, it adds them to the database via the `create` function in class `file`.

### delete(user)
Removes a user from the database.


## class wallet
Used for managing a user's wallet.
### get(user)
Gets the balance of a user's wallet.

### add(user, add)
Adds money to a user's wallet.

### remove(user, take)
Removes money from a user's wallet.


## class bank
Used for managing a user's bank.
### get(user)
Gets the balance of a user's bank.

### add(user, add)
Adds money to a user's bank.

### remove(user, take)
Removes money from a user's bank.


## class Eco
Some useful functions, typically for user interaction.
### deposit(user, amount)
Deposits money from a user's wallet to their bank.

### withdraw(user, amount)
Withdraws money from a user's bank to their wallet.

### rob(user, target)
Attempts to rob 1/5 of the money in somebody's wallet with a 20% chance of success. If successful, money is given to theif.

### pay(user, target, amount)
Sends money from one user to another.
