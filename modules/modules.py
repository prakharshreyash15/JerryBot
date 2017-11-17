# -*- coding: (utf8 -*-
from modules.roll import roll
from modules.flip import flip
from modules.menu import menu
from modules.hi import hi
from modules.choose import choose
from modules.weather import weather, jacket
from modules.tip import tip
from modules.translate import translate_text
from modules.rood import eatadick
from modules.barrelroll import doabarrelroll
from modules.snack import snack
from modules.poll import poll, vote, result, end
from modules.remind import remind
from modules.tag import tag
from modules.mini_modules import *
from modules.permissions import *
from modules.kick import kick
from modules.dunce import duncecap
from modules.quote import imagequote

help_string = ""

def help_message(args=[], perms={}):
    global help_string
    if help_string is "":
        result = "Commands:\n"
        for key in sorted(modules):
            result += "  !%s\n" % (key)
        help_string = result
    return help_string

"""command : (function"""
modules = {
    "roll": (roll, []),
    "flip": (flip, []),
    "help": (help_message, []),
    "menu": (menu, []),
    "fud": (menu, []),
    "food": (menu, []),
    "sustenance": (menu, []),
    "thanks": (thanks, []),
    "eatadick": (eatadick, []),
    "weather": (weather, []),
    "jacket": (jacket, []),
    "barrelroll": (doabarrelroll, []),
    "doabarrelroll": (doabarrelroll, []),
    "shrug": (shrug, []),
    "birb": (bird, []),
    "choose": (choose, []),
    "tip": (tip, []),
    "translate": (translate_text, []),
    "goodshit": (goodshit, []),
    "lenny": (lenny, []),
    "sleep": (sleep, []),
    "snack": (snack, []),
    "poll": (poll, [MESSAGE_THREADID, MESSAGE_TIME]),
    "vote": (vote, [MESSAGE_THREADID, USER_NAME]),
    "result": (result, [MESSAGE_THREADID]),
    "end": (end, [MESSAGE_THREADID]),
    "hi": (hi, [USER_NAME]),
    "remind": (remind, [MESSAGE_AUTHOR]),
    "tag": (tag, []),
    "kick": (kick, [MESSAGE_THREADID,
                    FN_GET_UID,
                    FN_REMOVEUSER,
                    SELF_UID]),
    "duncecap": (duncecap, [MESSAGE_THREADID,
                            THREAD_NICKNAMES,
                            FN_GET_UID,
                            FN_GET_NAME,
                            FN_SEND_MESSAGE,
                            FN_CHANGE_NICKNAME]),
    "quote": (imagequote, [MESSAGE_THREADID,
                           FN_SEND_IMAGE])
}
