# Events
A few event listeners that listen for things and when they hear things they do things.

## botjoin.py
Sends a message to the first available channel whenever the bot joins a server.

## counting.py
Listens for messages in the guild's counting channel, deletes messages if neccessary, and updates the guild's counting number accordingly.

## error.py
Listens for errors, and when one is raised, handles it accordingly.

## ready.py
Runs when the bot is ready, simply sets a custom status and prints a message.

## userjoin.py
Listens for a user joining a guild, check if they are supposed to be muted, and if so, adds the muterole to them again.