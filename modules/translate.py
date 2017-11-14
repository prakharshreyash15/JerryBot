from microsofttranslator import Translator
from modules.auth import MSFT_CLIENTID,MSFT_CLIENTSECRET
from modules.language_table import languages

translator = Translator(MSFT_CLIENTID, MSFT_CLIENTSECRET)

def to_iso(word):
    word_lower = word.lower()
    try:
        ret_iso = languages[word_lower]
        return ret_iso
    except:
        if word_lower in languages.values():
            return word_lower
        if word in languages.values():
            return word
    return ""


def translate_text(args=[], permisions = {}):
    global translator
    
    if args[0] == "help":
        return "!translate $from$>$to$ words"
    if len(args) == 1:
        try:
            lang = languages[args[0]]
            return "Code for %s: %s" %(args[0], lang)
        except:
            return "Not a language"
    langs = args[0].split("->")
    words = " ".join(args[1:])
    if len(langs) == 1:
        try:
            lang = to_iso(langs[0].lower())
            return translator.translate(words, lang)
        except:
            return "language not found"
    else:
        print(langs)
        try:
            from_lang = to_iso(langs[0])
            new_text = ""
            for i in range(len(langs)-1):
                to_lang = to_iso(langs[i+1])
                print("from %s to %s" %(from_lang, to_lang))
                if from_lang is not "" and to_lang is not "":
                    new_text = translator.translate(words, to_lang, from_lang)
                from_lang = to_lang
            return new_text
        except Exception as e:
            print("ERROR")
            print(str(e))
            return ""
