# i can't code in python without a struct

from reader import feedbuzz_file_read, ReaderSyntaxError
from test import FeedBuzzTest, FeedBuzzPlayer, test_check_validity, FeedBuzzException
from test import player_start_test, test_calculate_maximum, test_sort_ranges
from sys import stderr
from json import dumps
from os.path import isfile

CODENAME = "feedbuzz"

class Opts:
    def __init__(opts, input="", output="", maximum=False, ranges=False, questions=False):
        opts.input = input
        opts.output = output
        opts.maximum = maximum
        opts.ranges = ranges
        opts.questions = questions

class OptReadError(Exception):
    pass

def get_flag_value(flag_name, argv_over):
    try:
        value = next(argv_over)

        if value.startswith("--"):
            raise OptReadError(f"Flag {flag_name} is missing a value")
    except StopIteration:
        raise OptReadError(f"Flag {flag_name} is missing a value")

def read_opts(opts, argv):
    argv_over = iter(argv)
    next(argv_over) # skip over the first element of argv, which is main.py

    for arg in argv_over:
        if arg.startswith("--"):
            if arg == "--output":
                opts.output = get_flag_value(arg, argv_over)
            elif arg == "--maximum":
                opts.maximum = True
            elif arg == "--ranges":
                opts.ranges = True
            elif arg == "--questions":
                opts.questions = True
            elif arg == "--help":
                raise OptReadError(
                            "usage\n"
                            "          [input_file] [--output output_file] [--maximum]\n"
                            "          [--ranges] [--help]\n"
                            "\n"
                            "--output    Specify file path of JSON test reults\n"
                            "--questions Specify file path of JSON test reults\n"
                            "--maximum   Get maximum points possible in a test\n"
                            "--ranges    List all ranges in a test sorted.    \n"
                            "--help      Show this help message.              \n"
                            "\n"
                            "Refer to README.html to get full help.\n"
                        )
            else:
                raise OptReadError(f"Unknown flag: {arg}")

            continue

        if opts.input != "":
            raise OptReadError(f"Input already has been defined: {opts.input}")

        opts.input = arg


from test import player_start_anticipation, player_confront, test_results_json, player_is_finished

def test_start(opts, test, player):
    player_start_test(player)

    if not player_start_anticipation(test):
        return

    while player_confront(test, player):
        pass

    if not player_is_finished(player):
        return

    try:
        json = test_results_json(test, player)

        with open(opts.output, "w") as json_file:
            json_file.write(dumps(json))

        print(f"Results in JSON are written to {opts.output}")
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Failed to write results in JSON to {opts.output} ({e})")

def test_start_CURSES(win, opts, test, player):
    from display import feedbuzz_display_setup, feedbuzz_display_test_beginning

    feedbuzz_display_setup(win)
    feedbuzz_display_test_beginning(win, test)

def main(argv):
    opts = Opts(input="", output="a.json")

    try:
        read_opts(opts, argv)
    except OptReadError as error:
        print(f"{CODENAME}: {error}", file=stderr)
        return 1

    if not isfile(opts.input):
        print(f"{CODENAME}: no such test descriptive file: {opts.input}", file=stderr)
        return 1

    test = FeedBuzzTest(title="", description="", questions=[], ranges=[])

    with open(opts.input, "r") as test_file:
        try:
            feedbuzz_file_read(test, test_file)
        except ReaderSyntaxError as e:
            print(f"{CODENAME}: {e}", file=stderr)
            return 1

    try:
        test_check_validity(test)
        test_sort_ranges(test)
    except FeedBuzzException as e:
        print(f"{CODENAME}: {e}", file=stderr)
        return 1

    test.maximum_possible = test_calculate_maximum(test)

    if opts.maximum:
        print(f"{test.maximum_possible}")
        return 0
    elif opts.ranges:
        if not test.ranges:
            print("No score ranges in this test.")
            return 1

        print(f"Score ranges ({len(test.ranges)}):")

        for idx, (scorerange, previous) in enumerate(zip(test.ranges[1:], test.ranges)):
            print(f"{idx+1}. [{previous.at}~{scorerange.at}] {previous.description}")

        recent = test.ranges[-1]
        print(f"{len(test.ranges)}. [>={recent.at}] {recent.description}")

        return 0
    elif opts.questions:
        if not test.questions:
            print("No questions in this test.")
            return 1

        print(f"Questions ({len(test.questions)}):")

        for idx, question in enumerate(test.questions):
            print(f"{idx+1}. {question.contents}")

        return 0

    player = FeedBuzzPlayer(test)
    test_start(opts, test, player)

    return 0

if __name__ == "__main__":
    from sys import argv
    raise SystemExit(main(argv))
    # raise SystemExit(main(["main.py", "business.q"]))
