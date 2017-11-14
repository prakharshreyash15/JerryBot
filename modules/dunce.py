from modules.permissions import *
from time import sleep


def duncecap(args, perms={}):

    # Get name and uid of person
    name = " ".join(args)
    uid = perms[FN_GET_UID](name)

    # Get all nicknames in thread
    nicknames = perms[THREAD_NICKNAMES](perms[MESSAGE_THREADID])

    # Check that no one is currently the dunce
    for k, v in nicknames.items():
        if v == "Town Dunce":
            name = perms[FN_GET_NAME](k)
            return "%s is already the Town Dunce" % (name)
    # Store old nickname
    old_name = name
    if uid in nicknames:
        old_name = nicknames[uid]
    print(old_name, uid, perms[MESSAGE_THREADID])

    # Change to duncecap, send message
    perms[FN_CHANGE_NICKNAME]("Town Dunce", uid, perms[MESSAGE_THREADID])

    # Wait 10 minutes, then change their name back
    sleep(600)
    perms[FN_CHANGE_NICKNAME](old_name, uid, perms[MESSAGE_THREADID])
