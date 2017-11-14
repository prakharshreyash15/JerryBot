from modules.permissions import *

def hi(args, perms = {}):
    full_name = perms[USER_NAME]
    first = full_name.split()[0]
    return "Hi, " + first + "!"