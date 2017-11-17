import requests
import textwrap
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from modules.permissions import *
from typing import Text, Optional


def format_image(message: Text):
    r = requests.get("https://picsum.photos/800/600/?random", stream=True)
    if r.status_code == 200:
        img = Image.open(BytesIO(r.content))
        font = ImageFont.truetype("modules/fonts/font.ttf", 72)
        draw = ImageDraw.Draw(img)
        draw.text((100, 100), message, (255, 255, 255), font=font)
        img.save("image.jpg")


def imagequote(args=[], perms={}):
    words = " ".join(args)
    sections = words.split("-")
    message = sections[0].strip()
    if "|" in message:   
        message = message.replace("|", "\n")
    else:
        message = "\n".join(textwrap.wrap(message, 24))
    author = None
    try:
        author = sections[1].strip()
    except IndexError:
        author = "someone stupid"

    message = message + ("\n       -%s" %(author))
    format_image(message)
    perms[FN_SEND_IMAGE]("image.jpg", perms[MESSAGE_THREADID])
