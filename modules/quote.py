import requests
import textwrap
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from modules.permissions import *
from typing import Text, Optional


def format_image(message: Text, author: Optional[Text]):
    if author is None:
        author is "someone stupid"
    r = requests.get("https://picsum.photos/800/600/?random", stream=True)
    if r.status_code == 200:
        img = Image.open(BytesIO(r.content))
        formatted_text = "\n".join(textwrap.wrap(message, 24)) + ("\n       -%s" %(author))
        font = ImageFont.truetype("modules/fonts/font.ttf", 72)
        draw = ImageDraw.Draw(img)
        draw.text((100, 100), formatted_text, (255, 255, 255), font=font)
        img.save("image.jpg")


def imagequote(args=[], perms={}):
    words = " ".join(args)
    sections = words.split("-")
    message = sections[0].strip()
    author = None
    try:
        author = sections[1].strip()
    except IndexError:
        pass

    format_image(message, author)
    perms[FN_SEND_IMAGE]("image.jpg", perms[MESSAGE_THREADID])