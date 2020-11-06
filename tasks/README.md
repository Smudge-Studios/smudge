# Tasks
A few tasks that mostly have to do with moderation.

## bans.py
Checks for expired bans every minute, and if it finds one, unbans the user and sets `EXPIRED` to `True`.

## mutes.py
Checks for expired mutes every minute, and if it finds one, unmutes the user and sets `EXPIRED` to `True`.