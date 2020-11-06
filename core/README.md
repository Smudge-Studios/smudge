# Core
'Documentation' for bot cores.

This really isn't meant for use anywhere but this bot, as it's pretty much 100% hard coded.

## EcoCore
### class data
#### read()
Reads everything in the ECONOMY table in `economy.db`.

#### save()
Commits all changes to the database.



### class file
#### create(user)
Creates a new entry in the database.
##### Arguments
user: The ID of the user to be added to the database.



### class file2
#### check(user)
Checks if a user is in the database. If not, it adds them to the database via the `create` function in class `file`.
##### Arguments
user: The ID of the user to be checked.

#### delete(user)
Removes a user from the database.
##### Arguments
user: The ID of the user to be removed.



### class wallet
#### get(user)
Gets the balance of a user's wallet.
##### Arguments
user: The ID of the user whos balance is being retrieved.


#### add(user, add)
Adds money to a user's wallet.
##### Arguments
user: The user's ID.

add: The amount being added to `user`'s wallet.


#### remove(user, take)
Removes money from a user's wallet.
##### Arguments
user: The user's ID.

take: The amount being taken from `user`'s wallet.



### class bank
#### get(user)
Gets the balance of a user's bank.
##### Arguments
user: The ID of the user whos balance is being retrieved.


#### add(user, add)
Adds money to a user's bank.
##### Arguments
user: The user's ID.

add: The amount being added to `user`'s bank.


#### remove(user, take)
Removes money from a user's bank.
##### Arguments
user: The user's ID.

take: The amount being taken from `user`'s bank.



### class Eco
#### deposit(user, amount)
Deposits money from a user's wallet to their bank.
##### Arguments
user: The user's ID.

amount: The amount being deposited.


#### withdraw(user, amount)
Withdraws money from a user's bank to their wallet.
##### Arguments
user: The user's ID.

amount: The amount being withdrawn.


#### rob(user, target)
Attempts to rob 1/5 of the money in somebody's wallet with a 20% chance of success. If successful, money is given to theif.
##### Arguments
user: The user's ID.

target: The target's ID.


#### pay(user, target, amount)
Sends money from one user to another.
##### Arguments
user: The user's ID.

target: The target's ID.

amount: The amount of money being sent.
