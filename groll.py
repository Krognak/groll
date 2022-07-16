#!/usr/bin/env python3

# TODO refactor sub into 1 function
# TODO handle "cats"
# TODO argparse

import logging
import random
import re
import sys

__version__ = "0.1.0"

logging.basicConfig(level=logging.DEBUG)

DICE_SYNTAX = r"(?P<pre>[\+-/\*]?)(?P<die>\d*d\d+)(?P<post>[\+-/\*]?)"
MOD_SYNTAX = r"(?P<pre>[\+-/\*]?)(?P<mod>\d+)(?P<post>[\+-/\*]?)"

OPS = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
}


def roll(die: str) -> str:
    num, sides = die.split("d")
    if num:
        num = int(num)
    else:
        num = 1
    sides = int(sides)
    total = 0
    for _ in range(num):
        total += random.randint(1, sides)
    return str(total)


def sub_dice(args: list) -> list:
    """Substitute roll results into args and seperate any "sticky" operators"""
    subbed = []
    for arg in args:
        m = re.match(DICE_SYNTAX, arg)
        if m:
            mdict = m.groupdict()
            if mdict["pre"]:
                subbed.append(mdict["pre"])
            subbed.append(roll(mdict["die"]))
            if mdict["post"]:
                subbed.append(mdict["post"])
        else:
            subbed.append(arg)
    return subbed


def sub_int(args: list) -> list:
    subbed = []
    for arg in args:
        m = re.match(MOD_SYNTAX, arg)
        if m:
            mdict = m.groupdict()
            if mdict["pre"]:
                subbed.append(mdict["pre"])
            subbed.append(int(mdict["mod"]))
            if mdict["post"]:
                subbed.append(mdict["post"])
        else:
            subbed.append(arg)
    return subbed


def eval_roll(args: list) -> int:
    x, op, y, *rest = args
    while len(rest) > 0:
        x = OPS[op](x, y)
        op, y, *rest = rest
    x = OPS[op](x, y)
    return x


def cli() -> None:
    args = sys.argv[1:]
    logging.info(f"args supplied = {args}")
    args = sub_dice(args)
    logging.info(f"with dice subbed = {args}")
    args = sub_int(args)
    logging.info(f"with ints subbed = {args}")
    result = eval_roll(args)
    logging.info(f"answer = {result}")


if __name__ == "__main__":
    cli()
