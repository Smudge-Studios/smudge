class Exceptions(Exception):
    class Unable(Exception): # ALL: Unable to complete action
        pass
    class NEMT(Exception): # ECO: Target doesn't have enough money to be robbed.
        pass
    class NEMU(Exception): # ECO: You don't have enough money to rob someone.
        pass
    class FAIL(Exception): # ECO: Robbery was unsuccessful.
        pass
    class BLACKLISTED(Exception): # ECO: Specified user is blacklisted.
        pass

error = Exceptions()