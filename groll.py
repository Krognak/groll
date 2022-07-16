#!/usr/bin/env python3

# TODO refactor sub into 1 function
# TODO handle "cats"
# TODO argparse

import logging
import random
import re
import sys

from typing import Callable

__version__ = "0.1.0"

logging.basicConfig(level=logging.DEBUG)

re.DOTALL = True

DICE_SYNTAX = r"\d*d\d+"
MOD_SYNTAX = r"\d+"

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


def sub(args: list, pattern: str, func: Callable) -> list:
    subbed = []
    for arg in args:
        m = re.match(pattern, arg)
        if m:
            subbed.append(func(m.group(0)))
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
    args = " ".join(sys.argv[1:])
    args = re.sub(r"[\+-/\*]", lambda x: f" {x.group(0)} ", args)
    args = args.split()
    logging.info(f"tidied args = {args}")
    args = sub(args, DICE_SYNTAX, roll)
    logging.info(f"with dice subbed = {args}")
    args = sub(args, MOD_SYNTAX, int)
    logging.info(f"with ints subbed = {args}")
    result = eval_roll(args)
    logging.info(f"answer = {result}")


if __name__ == "__main__":
    cli()
