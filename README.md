# JerryBot

A Chat Bot for Facebook written using Python commands.  Uses a forked [fbchat](https://pypi.python.org/pypi/fbchat/) module with applied patches to get group chat working.

Written in Python3

##Installation

1. Clone Repo
2. Install `fbchat` and `microsofttranslator` from pip3


##Usage

`python JerryBot.py`

##Modules

Currently provided modules:
 * Flip (Flip a coin)
 * Roll (Roll an n sided die, default six)
 * Menu $day $dining_hall $meal (order of params shouldn't matter)
 * eatadick 
 * weather
 * jackets
 * helpgi
 * thanks
 
Planned Modules:
 * Reminders
 * Linkme/define
 * Random quote generation
 * Random joke generation
 * Combinatorial calculations
 
Create a module:

1. Create a module in modules/
2. Have one endpoint function that takes in a list of arguments (doesn't have to do anything with them)
3. Add function to modules{} in modules/modules.py
