# -*- coding: utf8 -*-
import requests
from modules.auth import TOKEN
import json
from datetime import datetime
from html.parser import HTMLParser

# Used to convert HTML codes to their characters
h = HTMLParser()

#dhalls = ['frary', 'frank', 'cmc', 'mudd', 'scripps', 'oldenborg', 'pitzer']
#meals = ['breakfast', 'lunch', 'dinner', 'brunch']
# days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'today']
#dhall_aliases = {'collins' : 'cmc', 'colins' : 'cmc', 'hoch' : 'mudd', 'malott' : 'scripps', 'malot': 'scripps', 'oldie' : 'oldenborg', 'old' : 'oldenborg', 'mcconnel' : 'pitzer', 'mcconnell' : 'pitzer'}
#day_aliases = {'m' : 'mon', 'monday' : 'mon', 't' : 'tue', 'tuesday' : 'tue', 'w': 'wed', 'wednesday' : 'wed', 'r' : 'thu', 'thursday' : 'thu', 'f' : 'fri', 'friday':'fri'}

def get_day(day):
    return {
        0 : 'mon',
        'mon' : 'mon',
        'monday' : 'mon',
        'm' : 'mon',

        1 : 'tue',
        'tue' : 'tue',
        'tuesday' : 'tue',
        'tues' : 'tue',
        't': 'tue',

        2 : 'wed',
        'wed' : 'wed',
        'wednesday' : 'wed',
        'w' : 'wed',

        3 : 'thu',
        'thu' : 'thu',
        'thursday' : 'thu',
        'thurs' : 'thu',
        'r' : 'thu',

        4 : 'fri',
        'fri': 'fri',
        'friday' : 'fri',
        'f' : 'fri',

        5 : 'sat',
        'sat' : 'sat',
        'saturday' : 'sat',
        's' : 'sat',

        6 : 'sun',
        'sun' : 'sun',
        'sunday' : 'sun',
        's' : 's',

        }.get(day, -1)

def get_dhall(dhall):
    return {
        'frank': 'frank',
        'frunk': 'frank',

        'oldenborg': 'oldenborg',
        'oldie' : 'oldenborg',
        'old' : 'oldenborg',

        'frary': 'frary',

        'cmc' : 'cmc',
        'collins' : 'cmc',

        'mudd' : 'mudd',
        'hoch' : 'mudd',
        'shan' : 'mudd',

        'scripps' : 'scripps',
        'malott' : 'scripps',
        'malot' : 'scripps',
        'scripts' : 'scripps',
        'scrips' :'scripps',

        'pitzer' : 'pitzer',
        'mcconnell' : 'pitzer',
        'mcconnel' : 'pitzer'
    }.get(dhall, -1)

def get_meal(meal):
    return {
        'breakfast' : 'breakfast',
        'b' : 'breakfast',
        'break' : 'breakfast',

        'lunch' : 'lunch',
        'l' : 'lunch',

        'dinner' : 'dinner',
        'd' : 'dinner',

        'brunch' : 'brunch',
        'r' : 'brunch',
        'br' : 'brunch'
    }.get(meal, -1)

def parse_input(in_text):
    # Check each of the input words, determine what's what

    #set defaults
    dhall = 'frary'
    meal = wat_meal()
    day = get_day(datetime.weekday(datetime.today()))

    #format text
    in_text = [i.lower().strip() for i in in_text]
    for w in in_text:

        #try on each dictionary lookup
        r_day = get_day(w)
        r_hall = get_dhall(w)
        r_meal = get_meal(w)

        #change if default value was not returned
        day = r_day if r_day is not -1 else day
        dhall = r_hall if r_hall is not -1 else dhall
        meal = r_meal if r_meal is not -1 else meal

    return dhall, day, meal

def get_menu(dhall, day, meal):
    url = 'https://aspc.pomona.edu/api/menu/dining_hall/' + dhall + '/day/' + day + '/meal/' + meal
    req = requests.get(url , params={'auth_token' : TOKEN})
    try:
        j = json.loads(req.text)
    except:
        return ["ASPC is down :("]
    food = []
    food.append('~*~' + dhall + '~*~')
    food.append('~*~' + day + '~*~')
    food.append('~*~' + meal + '~*~')
    try:
        for f in j[0]['food_items']:
            food.append(str(f))
        return food
    except:
        print("err")
        return []

def wat_meal():
    rn = datetime.now()
    day = get_day(datetime.weekday(datetime.today()))
    if day is 'sat' or day is 'sun':
        if rn.hour <= 14:
            meal = 'brunch'
        else:
            meal = 'dinner'
    elif rn.hour <= 10:
        # Breakfast before 10am
        meal = 'breakfast'
    elif rn.hour > 10 and rn.hour < 14:
        meal = 'lunch'
    elif rn.hour >= 14 and rn.hour <= 20:
        meal = 'dinner'
    else:
        # breakfast the next day if > 20
        meal = 'breakfast'

    return meal

def map_html_unencode(lst):
    temp = []
    for s in lst:
        temp.append(str(h.unescape(s)))
    return temp

def menu(args, perms={}):
    dhall, day, meal = parse_input(args)
    food = get_menu(dhall, day, meal)
    if len(food) > 0:
        return ('\n'.join(food).encode('utf-8').strip())
    return "No menu"
