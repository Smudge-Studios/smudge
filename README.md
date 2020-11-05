# Smudge
The official bot for Smudge Studios, developed by [@plun1331](https://plun1331.github.io).

This bot has not been tested yet.

## How to run
Clone this repository to your computer, place your Discord bot's token in `config.ini`, and execute `main.py`.

## Commands
### Utility
These commands are for utility purposes and can be used by anybody.

- `ping` - Check the bot's latency.

- `report <member> <reason>` - Report a user for violation of server rules.

- `suggest <suggestion>` - Make a suggestion to the server.

- `userinfo [member]` - Display information on a user, or yourself if no user is specified.

- `serverinfo` - Displays information on the guild the command was ran in.

### Fun
These commands are purely for fun and can be used by all users.

- `meme` - Display a random meme from [r/memes](https://reddit.com/r/memes/).

- `clap <text>` - Put👏clap👏emojis👏between👏words.

- `hack <member>` - Hack someone.

- `8ball <question>` - Ask the 8ball a question.

- `imposter <member>` - Are they an imposter?

- `say <message>` - Make the bot say something.

### Economy
These commands can be used by all, but can also be disabled for a specific user by a bot owner.

- `beg` - Beg for money.

- `balance [member]` - Check somebody's balance, or your own if member isn't specified.

- `daily` - Claim your daily reward.

- `deposit <amount|all>` - Deposit money from your wallet to your bank.

- `withdraw <amount|all>` - Withdraw money from your bank to your wallet.

- `rob <member>` - Attempt to rob from someone's wallet. 

- `pay <member> <amount>` - Pay someone some money.

- `work` - Do some work and get paid for it.

### Moderation
These commands are restricted to specific permissions.

- `muterole <role|create>` - Specify a mute role, or have the bot create one.

- `warn <member> [reason]` - Sends a warning to a user.

- `mute <member> [duration] [reason]` - Mutes someone with an optional duration.

- `ban <member> [duration] [reason]` - Bans someone with an optional duration.

- `kick <member> [reason]` - Kicks a member.

- `purge [number]` - Bulk deletes a number of messages in a channel. Limit of 100 messages.

- `unban <member>` - Unban the specified user from the guild.

- `unmute <member>` - Unmutes the specified user.

- `listpunishments <member> [warn|mute|kick|ban]` - Displays a list of punishments a member has recieved.

- `punishmentinfo <punishment ID>` - Displays information on a specific punishment.

- `deletepunishment <punishment ID>` - Deletes a punishment. This action is irreversable.

### Server
These commands are mostly restricted to guild managers.

- `prefix [prefix]` - Sets the server's prefix. Defaults to `>` if no prefix is specified.

- `count <channel|create|remove>` - Specify a channel for users to count in, have the bot create one.

- `suggestionchannel <channel|create|remove>` - Define a suggestion channel, or have the bot create one.

- `reportchannel <channel|create|remove>` - Define a reports channel, or have the bot create one.

### Restricted
These commands are restricted to the bot's owner.

- `wipe <member> [reason]` - Reset a user's balance in the economy.

- `blacklist <member> [reason]` - Blacklist someone from the economy.

- `unblacklist <member>` - Unblacklist someone from the economy.

- `addmoney <member> <amount> [wallet|bank]` - Add money to someone's wallet or bank.

- `removemoney <member> <amount> [wallet|bank]` - Remove money from someone's wallet or bank.

- `load <extension>` - Load a discord.py extension

- `unload <extension>` - Unload a discord.py extension

- `reload <extension>` - Reload a discord.py extension

- `stop` - Shutdown the bot.

### Other
WIP

## Data Storage
Bot data is stored within multiple SQLite3 databases, found in `data/`.

## Requirements
This project requires discord.py. You can install it by running the commands shown below on your respective operating system.
```sh
# Linux/macOS
python3 -m pip install -U discord.py

# Windows
py -3 -m pip install -U discord.py
```

