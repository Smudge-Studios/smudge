# Core
'Documentation' for bot cores.

This really isn't meant for use anywhere but this bot, as it's pretty much 100% hard coded.

# Quick Links
[EcoCore](https://github.com/Smudge-Studios/smudge/tree/main/core#ecocore)

[Exceptions](https://github.com/Smudge-Studios/smudge/tree/main/core#exceptions)

[ModCore](https://github.com/Smudge-Studios/smudge/tree/main/core#modcore)

[UtilCore](https://github.com/Smudge-Studios/smudge/tree/main/core#utilcore)

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



# Exceptions
Some custom exceptions
## class Exceptions
A few custom exceptions for the bot.
### class Unable
Unable to complete action. Is mostly used for passing custom error text from a core to a cog file.

### class NEMT
Signifies that the target does not have enough money.

### class NEMU
Signifies that the command invoker doesn't have enough money.

### class FAIL
Was made to signify that a robbery failed.

### class BLACKLISTED
Really no point to this, I started using discord.py's `commands.DisabledCommand` exception instead.



# ModCore
A few moderation utilities.
## thstndrd(number)
Used for adding 'th', 'st', 'nd', or 'rd' onto the end of intergers.

## class Mod
The Moderation class.
### gettime(time)
Converts a user inputted time value (7d, 1w, etc.) into seconds.

### ban(ctx, member, reason, duration)
Adds a user to the bot's 'BANS' table in `moderation.db`.

### kick(ctx, member, reason)
Adds a user to the bot's 'KICKS' table in `moderation.db`.

### mute(ctx, member, reason, duration)
Adds a user to the bot's 'MUTES' table in `moderation.db`.

### warn(ctx, member, reason)
Adds a user to the bot's 'WARNS' table in `moderation.db`.

### unban(ctx, member)
Sets `EXPIRED=TRUE` in the 'BANS' table in `moderation.db` for the specified user.

### unmute(ctx, member)
Sets `EXPIRED=TRUE` in the 'MUTES' table in `moderation.db` for the specified user.

### fetchpunishlist(ctx, member, type)
Fetches all punishments given to a specific user of an optional type.

### delpunish(ctx, id)
Deletes a punishment using the punishment's ID.

# UtilCore
Mostly configuration editing for servers.
## class Utils
Server utils.
### reportchannel(ctx)
Fetches the report channel for the guild you are currently in.

### suggestchannel(ctx)
Fetches the suggestions channel for the guild you are currently in.

### poll(input)
Returns a question and a list of options for the poll command.
