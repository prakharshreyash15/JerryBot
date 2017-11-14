from modules.permissions import *


def kick(args, perms={}):
    # Get fbid of person with $name
    name = " ".join(args)
    uid = perms[FN_GET_UID](name)

    # Kick from group if they aren't me
    if uid != perms[SELF_UID]:
        perms[FN_REMOVEUSER](uid, perms[MESSAGE_THREADID])
    else:
        return "No, screw you"
