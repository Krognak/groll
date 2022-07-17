#!/usr/bin/env python3

import argparse
import logging
import random
import re
import sys
import textwrap

from typing import Callable

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
    logging.debug(f"sub made using {func.__name__} -> {subbed}")
    return subbed


def eval_roll(args: list) -> None:
    try:
        if len(args) == 1:
            x = args[0]
        else:
            x, op, y, *rest = args
            while len(rest) > 0:
                x = OPS[op](x, y)
                op, y, *rest = rest
            x = OPS[op](x, y)
            logging.debug(f"answer = {x}")
        print("  -> ", x)
    except Exception as e:
        logging.debug(e, exc_info=True)
        print("  !!! unable to parse input, type groll -h for help !!!")


def tidy_args(args: list) -> list:
    args = " ".join(args)
    # finds "sticky" operators and spaces them out
    args = re.sub(r"[\+-/\*]", lambda x: f" {x.group(0)} ", args)
    args = args.split()
    logging.debug(f"tidied args = {args}")
    return args


def handle_dice(dice: list) -> list:
    dice = tidy_args(dice)
    dice = sub(dice, r"\d*d\d+", roll)
    dice = sub(dice, r"\d+", int)
    return dice


def handle_flags(flags: list) -> None:
    if "version" in flags:
        print(f"  groll v{__version__}")
        logging.debug("printing version and exiting")
        sys.exit()


def get_parser():
    parser = argparse.ArgumentParser(
        prog="groll",
        usage="groll [options] [dice ...]",
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent(
            """\
            A helpful, dice rolling goblin for your command line!

        Syntax:
          dice = [num]d[sides] e.g. 2d36
          supported operators = +, -, *, /
          modifiers = integer numbers"""
        ),
        epilog=textwrap.dedent(
            """\
        Examples:
          $ groll <- rolls 1d20 when supplied with no args
          $ groll 2d6 + 2 <- rolls 2d6 and adds 2 to the result
          $ groll 1d4 + 2d10 / 2 <- adds a d4 to a 2d10 and halves the result"""
        ),
    )
    parser.add_argument("dice", nargs="*", help="dice and modifiers")
    parser.add_argument(
        "-l", "--logging", action="store_true", help="enable debugging messages"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_const",
        const="version",
        dest="flags",
        help="display version number and exit",
    )
    return parser


# entrypoint for groll to be specified in pyproject.toml
def cli() -> None:
    parser = get_parser()
    args = parser.parse_args()
    if args.logging:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.debug("Starting...")
    if args.flags:
        handle_flags(args.flags)
    if not args.dice:
        args.dice = ["d20"]
    dice = handle_dice(args.dice)
    logging.debug("...Finished")
    eval_roll(dice)


if __name__ == "__main__":
    cli()
