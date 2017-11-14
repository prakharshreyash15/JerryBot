from modules.permissions import *
from time import sleep


def duncecap(args, perms={}):
    print("In duncecap")
    name = " ".join(args)
    uid = perms[FN_GET_UID](name)

    print(perms[MESSAGE_THREADID])
    print(perms[THREAD_NICKNAMES])
    nicknames = perms[THREAD_NICKNAMES](perms[MESSAGE_THREADID])

    for k, v in nicknames.items():
        if v == "Town Dunce":
            name = perms[FN_GET_NAME](k)
            perms[FN_SEND_MESSAGE](f"{name} is already the Town Dunce", perms[MESSAGE_THREADID])
            return ""

    print("names")
    old_name = name
    if uid in nicknames:
        old_name = nicknames[uid]
    print(old_name, uid, perms[MESSAGE_THREADID])

    perms[FN_CHANGE_NICKNAME]("Town Dunce", uid, perms[MESSAGE_THREADID])

    perms[FN_SEND_MESSAGE](f"{name} is now the Town Dunce", perms[MESSAGE_THREADID])

    sleep(600)
    perms[FN_CHANGE_NICKNAME](old_name, uid, perms[MESSAGE_THREADID])
    perms[FN_SEND_MESSAGE](f"{name} is no longer the Town Dunce", perms[MESSAGE_THREADID])
