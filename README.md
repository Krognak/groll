# Groll

*A helpful, dice rolling goblin for your command line!*

```bash
$ groll 1d10 + 4
  -> 7
```

## Contents

* [Installation](#installation)

* [Usage](#usage)

* [TODO](#todo)

## Installation

```bash
$ pip install groll
```

## Usage

```bash
usage: groll [options] [dice ...]

Syntax:
  dice = [num]d[sides] e.g. 2d36
  supported operators = +, -, *, /
  modifiers = integer numbers

positional arguments:
  dice           dice and modifiers

options:
  -h, --help     show this help message and exit
  -l, --logging  enable debugging messages
  -v, --version  display version number and exit

Examples:
  $ groll <- rolls 1d20 when supplied with no args
  $ groll 2d6 + 2 <- rolls 2d6 and adds 2 to the result
  $ groll 1d4 + 2d10 / 2 <- adds a d4 to a 2d10 and halves the result
```

## TODO

- [ ] pyproject.toml
- [ ] nox
- [ ] crits
- [ ] exploding dice
