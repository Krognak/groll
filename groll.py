#!/usr/bin/env python3

# TODO argparse

import logging
import random
import re
import sys

from typing import Callable

__version__ = "0.1.0"

logging.basicConfig(level=logging.DEBUG)

OPS = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
}


def roll(die: str) -> str:
    num, sides = die.split("d")
    # because we don't always write 1d6...
    if num:
        num = int(num)
    else:
        num = 1
    sides = int(sides)
    total = 0
    for _ in range(num):
        total += random.randint(1, sides)
    return str(total)


def sub(args: list, pattern: list, func: Callable) -> list:
    subbed = []
    for arg in args:
        m = re.match(pattern, arg)
        if m:
            subbed.append(func(m.group(0)))
        else:
            subbed.append(arg)
    logging.info(f"sub made using {func.__name__} -> {subbed}")
    return subbed


def eval_roll(args: list) -> None:
    try:
        x, op, y, *rest = args
        while len(rest) > 0:
            x = OPS[op](x, y)
            op, y, *rest = rest
        x = OPS[op](x, y)
        logging.info(f"answer = {x}")
        return x
    except Exception as e:
        logging.critical(e, exc_info=True)


def tidy_args(args: list) -> list:
    args = " ".join(args)
    # finds "sticky" operators and spaces them out
    args = re.sub(r"[\+-/\*]", lambda x: f" {x.group(0)} ", args)
    args = args.split()
    logging.info(f"tidied args = {args}")
    return args


# entrypoint for groll to be specified in pyproject.toml
def cli() -> None:
    logging.info("Starting...")
    args = tidy_args(sys.argv[1:])
    args = sub(args, r"\d*d\d+", roll)
    args = sub(args, r"\d+", int)
    eval_roll(args)


if __name__ == "__main__":
    cli()
    logging.info("...Finished")
