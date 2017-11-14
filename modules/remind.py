from modules.menu import menu
from time import sleep
from datetime import datetime
import re

def remind(args, perms = {}):
    # get time right now 
    rn = datetime.now()

    # get the menu from where you want
    food = menu(args[1:], perms)
    
    l = map(int, re.findall('\d+', args[0]))
    try:
        assert len(l) <= 2
    except:
        return 'Invalid time input!'

    if 'pm' in args[0]:
        l[0] += 12
    
    want_dt = datetime(rn.year, rn.month, rn.day, l[0], l[1])

    if want_dt > rn:
        sleep_time = (want_dt - rn).total_seconds()
        sleep(sleep_time)
        return food
