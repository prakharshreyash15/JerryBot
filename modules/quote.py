import requests
import textwrap
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from modules.permissions import *
from typing import Text
from os import path
import random
from shutil import move, copy
import traceback

quoteboard_fonts = [
    "AmaticSC-Regular.ttf",
    "cac_champagne.ttf",
    "Pacifico.ttf",
    "MonotypeCorsiva.ttf",
    "Raleway-Black.ttf"
]

coordinates = [
    (101, 101),
    (100, 101),
    (99, 101),
    (101, 100),
    (99, 100),
    (101, 99),
    (100, 99),
    (99, 99)
]

BOARD_DEFAULT_WIDTH = 4000
BOARD_DEFAULT_HEIGHT = 3000
BOARD_DEFAULT_MARGIN = 200


def add_to_quoteboard(messages, thread_id,
                      width=BOARD_DEFAULT_WIDTH,
                      height=BOARD_DEFAULT_HEIGHT,
                      margin=BOARD_DEFAULT_MARGIN):
    quoteboard_path = path.join("modules", "data",
                                "%s_quoteboard.jpg" % (thread_id))
    print("adding to quoteobard")
    print(messages)
    if not path.exists(quoteboard_path):
        print('making quoteboard')
        img = Image.new('RGB', (width, height), (255, 255, 255))
        img.save(quoteboard_path)
    img = Image.open(quoteboard_path)
    draw = ImageDraw.Draw(img)
    for message in messages:
        print("Adding %s" % (message))
        font_path = path.join("modules", "fonts",
                              random.choice(quoteboard_fonts))
        font = ImageFont.truetype(font_path, random.randint(24, 54))

        draw.text((random.randint(50, width - margin),
                  random.randint(50, height - margin)),
                  message, (0, 0, 0), font=font)
        img.save(quoteboard_path)


def format_image(message: Text, thread_id: Text,
                 pic_path=None):
    img = None
    print("hello")
    if pic_path is None:
        print("fetching image")
        r = requests.get("https://picsum.photos/800/600/?random", stream=True)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
    else:
        print(pic_path)
        img = Image.open(pic_path)
    img.save(path.join("modules", "data", "%s_last.jpg" % (thread_id)))
    font = ImageFont.truetype("modules/fonts/MonotypeCorsiva.ttf", 72)
    draw = ImageDraw.Draw(img)
    for coords in coordinates:
        draw.text(coords, message, (0,0,0), font=font)
    draw.text((100, 100), message, (255,255,255), font=font)
    print("done")
    img.save("image.jpg")


def imagequote(args=[], perms={}, send_image=True, requote=False):
    words = " ".join(args)
    sections = words.split("-")
    message = sections[0].strip()
    if "|" in message:
        message = message.replace("|", "\n")
    else:
        message = "\n".join(textwrap.wrap(message, 24))
    author = "anonymous"
    try:
        author = sections[1].strip()

    except IndexError:
        pass
    message = message + ("\n       -%s" % (author))
    add_to_quoteboard([message.replace("|", " ")], perms[MESSAGE_THREADID])

    with open(path.join("modules",
                        "data",
                        "%s_quotes.txt" % (perms[MESSAGE_THREADID])), 'a') as f:
        f.write("%s|%s\n" % (sections[0].replace("|","  ").replace("\n", " ").strip(), author))

    if send_image:
        if requote:
            format_image(message, perms[MESSAGE_THREADID],
                         path.join("modules", "data",
                                   "%s_last.jpg" % (perms[MESSAGE_THREADID])))
        else:
            format_image(message, perms[MESSAGE_THREADID])

        perms[FN_SEND_IMAGE]("image.jpg", perms[MESSAGE_THREADID])


# same quote, diff image
def reroll(args=[], perms={}):

    with open(path.join("modules",
                        "data",
                        "%s_quotes.txt" % (perms[MESSAGE_THREADID])), 'r') as f:

        quotes = f.read().split("\n")[:-1]
        last_quote = quotes[-1]
        sections = last_quote.split("|")
        last_message = sections[0]
        last_author = sections[1]
        message = "\n".join(textwrap.wrap(last_message, 24)) + ("\n       -%s" % (last_author))
        format_image(message, perms[MESSAGE_THREADID])

        perms[FN_SEND_IMAGE]("image.jpg", perms[MESSAGE_THREADID])


# same image, diff quote
def requote(args=[], perms={}):
    imagequote(args, perms, requote=True)


def savequote(args=[], perms={}):
    imagequote(args, perms, False)
    return "Saved quote!"


def quotes(args=[], perms={}):
    with open(path.join("modules",
                        "data",
                        "%s_quotes.txt" % (perms[MESSAGE_THREADID])), 'r') as f:

        content = f.read()
        lines = content.split("\n")[:-1]
        print(lines)
        quotes = random.sample(lines, min(5, random.randint(1, len(lines))))
        formatted_quotes = []
        for q in quotes:
            sections = q.split("|")
            formatted_quotes.append("%s - %s" %(sections[0], sections[1]))
    return "\n".join(formatted_quotes)


def quoteboard(args=[], perms={}):

    quoteboard_path = path.join("modules", "data",
                                "%s_quoteboard.jpg" % (perms[MESSAGE_THREADID]))
    copy(quoteboard_path, "image.jpg")
    perms[FN_SEND_IMAGE]("image.jpg", perms[MESSAGE_THREADID])


def photo(args=[], perms={}):
    copy(path.join("modules", "data", "%s_last.jpg" % (perms[MESSAGE_THREADID])), "image.jpg")
    perms[FN_SEND_IMAGE]("image.jpg", perms[MESSAGE_THREADID])


def refresh_quoteboard(args=[], perms={}):

    quoteboard_path = path.join("modules", "data",
                                "%s_quoteboard.jpg" % (perms[MESSAGE_THREADID]))
    with open(path.join("modules",
                        "data",
                        "%s_quotes.txt" % (perms[MESSAGE_THREADID])), 'r') as f:

        content = f.read()
        quotes = content.split("\n")[:-1]
        formatted_quotes = []
        for q in quotes:
            sections = q.split("|")
            quote = "\n".join(textwrap.wrap(sections[0], random.randint(20, 60)))
            formatted_quotes.append('%s\n       -%s' %(quote, sections[1]))
        if path.exists(quoteboard_path):
            move(quoteboard_path,
                 path.join("modules", "data",
                           "%s_quoteboard_old.jpg" % (perms[MESSAGE_THREADID])))
        if len(args) is 0:
            add_to_quoteboard(formatted_quotes, perms[MESSAGE_THREADID])
        elif len(args) is 3:
            print(args)
            add_to_quoteboard(formatted_quotes, perms[MESSAGE_THREADID],
                              int(args[0]),
                              int(args[1]),
                              int(args[2]))
        else:
            return "Invalid parameters for new quoteboard - specify width height margin"
        copy(quoteboard_path, "image.jpg")
        # perms[FN_SEND_IMAGE]("image.jpg", perms[MESSAGE_THREADID])
