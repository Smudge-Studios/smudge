# Data
Data for the bot is stored within multiple SQLite3 Databases.

This is a list of databases and their purposes

Formatted as:
# `DataBase File`
Description of database.

## Table
Description of table.

### Value within table
Description of table value.


# Useful Resources
[SQLite3 Downloads](https://www.sqlite.org/download.html)

[SQLite Studio](https://github.com/pawelsalawa/sqlitestudio/releases)


# `bot.db`
This database is used for storing global bot config.


## BLACKLIST
A list of blacklisted users.

### USER
The ID of the blacklisted user.

### REASON
The reason a user was blacklisted.



# `config.db`
This database is used for storing guild-specific configuration.


## CONFIG
Guild prefix and channel settings.

### GUILD
The guild ID that the configuration belongs to.

### PREFIX
The guild's bot prefix.

### SUGGESTIONS
The guild's set suggestion channel's ID.

### REPORTS
The guild's set report channel's ID.



## COUNTING
Guild counting data.

### GUILD
The guild ID that the counting config belongs to.

### CHANNEL
The guild's counting channel's ID.

### NUMBER
The number the guild has counted to.



# `economy.db`
This database is used for storing data about the economy (user's balances, etc.)


## ECONOMY
### USER
The ID of the user the balances belong to.

### WALLET
The balance of the user's wallet.

### BANK
The balance of the user's bank.



# `moderation.db`
This database is used for storing moderation information.


## BANS
A list of bans issued using the bot.

### GUILD
The ID of the guild that the ban was issued from.

### USER
The ID of the user that was banned.

### REASON
The reason a user was banned for.

### MOD
The moderator that issued the ban.

### ID
The punishment ID. Nothing special here.

### EXPIRES
The time the punishment expires. This value is stored in seconds, and can also be 'Permanent'.

### EXPIRED
A boolean value that indicates whether or not the ban has expired.



## CONFIG
The guild's moderation configuration.

### GUILD
The ID of the guild the config belongs to.

### MUTEROLE
The ID of the role that is used to mute people in that guild.



## KICKS
A list of kicks issued using the bot.

### GUILD
The ID of the guild that the kick was issued from.

### USER
The ID of the user that was kicked.

### REASON
The reason a user was kicked for.

### MOD
The moderator that issued the kick.

### ID
The punishment ID.



## MUTES
A list of mutes issued using the bot.

### GUILD
The ID of the guild that the mute was issued from.

### USER
The ID of the user that was muted.

### REASON
The reason a user was muted for.

### MOD
The moderator that issued the mute.

### ID
The punishment ID.

### EXPIRES
The time the punishment expires.

### EXPIRED
A boolean value that indicates whether or not the mute has expired.



## PUNISHMENTS
A table containing the number of punishments issued using the bot.

### WARNS
The number of warns issued using the bot.

### MUTES
The number of mutes issued using the bot.

### KICKS
The number of kicks issued using the bot.

### BANS
The number of bans issued using the bot.

### TOTAL
The total number of punishments issued using the bot. This value is also used to get punishment IDs.



## WARNS
A list of warns issued using the bot.

### GUILD
The ID of the guild that the warning was issued from.

### USER
The ID of the user that was warned.

### REASON
The reason a user was warned for.

### MOD
The moderator that issued the warning.

### ID
The punishment ID.
