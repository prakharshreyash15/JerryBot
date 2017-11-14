import requests
from modules.auth import WEATHER_TOKEN
import json
from datetime import datetime

current_weather = {}
current_time = datetime.now()
hot_temp = (70, 100)
cool_temp = (60, 70)
chilly_temp = (50, 60)
coldaf_temp = (0, 50)
no_wind = (0, 10)
some_wind = (10, 20)
many_wind = (20, 100)

def in_range(x, var):
    (a,b) = var
    return (x >= a and x < b)

def temp_change(t):
    return "%.2f" %((float(t)*9/5.0)-459.67)

def should_update():
    global current_weather
    global current_time
    time_diff = datetime.now() - current_time
    if (time_diff.total_seconds() / 60) >= 10 or current_weather == {}:
        current_time = datetime.now()
        current_weather = get_weather()
        return True
    return False

def get_weather(city="Claremont"):
    url = "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s" %(city, WEATHER_TOKEN)
    req = requests.get(url)
    j = json.loads(req.text)
    return j

def weather(args, permisions = {}):
    global current_weather

    if len(args) < 1:
        should_update()
        return "Weather:\n%s/%s\nTemp: %s\nMin: %s Max: %s" %(current_weather["weather"][0]["main"],
                                                        current_weather["weather"][0]["description"],
                                                        temp_change(current_weather["main"]["temp"]),
                                                        temp_change(current_weather["main"]["temp_min"]),
                                                        temp_change(current_weather["main"]["temp_max"]))

    else:
        loc_weather = get_weather(city=" ".join(args))
        return "Weather in %s:\n%s/%s\nTemp: %s\nMin: %s Max: %s" %(" ".join(args),
                                                        loc_weather["weather"][0]["main"],
                                                        loc_weather["weather"][0]["description"],
                                                        temp_change(loc_weather["main"]["temp"]),
                                                        temp_change(loc_weather["main"]["temp_min"]),
                                                        temp_change(loc_weather["main"]["temp_max"]))


def jacket(args, permisions = {}):
    global current_weather
    global hot_temp, cool_temp, chilly_temp
    global no_wind, some_wind, many_wind
    should_update()
    temp = float(temp_change(current_weather["main"]["temp"]))
    speed = float(current_weather["wind"]["speed"])
    res_string = ""
    if in_range(temp, hot_temp):
        res_string = "It's hot out, "
    elif in_range(temp, cool_temp):
        res_string = "It's pretty brisk out, "
    elif in_range(temp, chilly_temp):
        res_string = "It's pretty chilly out, "
    elif in_range(temp, coldaf_temp):
        res_string = "It's really cold outside, "
    else:
        res_string = "It's burning outside, "

    if in_range(speed, no_wind):
        if not in_range(temp, hot_temp):
            res_string = res_string + "but not windy."
        else:
            res_stirng = res_string + "and not windy."
    elif in_range(speed, some_wind):
        res_string = res_string + "and there's a breeze outside."
    elif in_range(speed, many_wind):
        res_string = res_string + "and it's windy outside."
    else:
        res_string = res_string + "and there's a hurricane."

    if not in_range(temp, hot_temp) or not in_range(speed, no_wind):
        res_string = "You need a jacket.\n" + res_string
    else:
        res_string = "You don't need a jacket.\n" + res_string

    return res_string


