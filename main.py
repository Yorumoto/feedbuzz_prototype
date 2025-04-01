# i can't code in python without a struct

from reader import feedbuzz_file_read, ReaderSyntaxError
from test import FeedBuzzTest, FeedBuzzPlayer, test_check_validity, FeedBuzzException
from test import player_start_test
from sys import stderr
from os.path import isfile

CODENAME = "feedbuzz"

class Opts:
    def __init__(opts):
        opts.input = ""
        opts.preset = ""

class OptReadError(Exception):
    pass

def read_opts(opts, argv):
    argv_over = iter(argv)
    next(argv_over) # skip over the first element of argv, which is main.py

    for arg in argv_over:
        if arg.startswith("--"):
            continue

        if opts.input != "":
            raise OptReadError(f"Input already has been defined: {opts.input}")

        opts.input = arg


def test_start(test, player):
    player_start_test(player)

def main(argv):
    opts = Opts()

    try:
        read_opts(opts, argv)
    except OptReadError as error:
        print(f"{CODENAME}: {error}", file=stderr)
        return 1

    if not isfile(opts.input):
        print(f"{CODENAME}: no such test descriptive file: {opts.input}", file=stderr)
        return 1

    test = FeedBuzzTest(questions=[], ranges=[])

    with open(opts.input, "r") as test_file:
        try:
            feedbuzz_file_read(test, test_file)
        except ReaderSyntaxError as e:
            print(f"{CODENAME}: {e}", file=stderr)
            return 1

    try:
        test_check_validity(test)
    except FeedBuzzException as e:
        print(f"{CODENAME}: {e}", file=stderr)
        return 1

    player = FeedBuzzPlayer(test)
    test_start(test, player)

    return 0

if __name__ == "__main__":
    # from sys import argv
    # raise SystemExit(main(argv))
    raise SystemExit(main(["main.py", "basic.q"]))
