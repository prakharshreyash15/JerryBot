from random import randint


def flip(args, permisions={}):
    res = randint(1, 2)
    if res == 1:
        return "Flipped a coin: Heads"
    else:
        return "Flipped a coin: Tails"
