from datetime import datetime, timedelta
datetime_now = datetime.now

class FeedBuzzException(Exception):
    pass

class FeedBuzzAnswer:
    def __init__(answer, contents="", description="", score=0, toggled=False):
        answer.contents = contents
        answer.description = ""
        answer.score = 0
        answer.toggled = toggled

def answer_unwrap(answer):
    assert type(answer) is FeedBuzzAnswer, "answer_unwrap failed assertion"

class FeedBuzzQuestion:
    def __init__(question, contents="", answers=None, multi_choice=False):
        if answers is None:
            answers = []

        question.contents = contents
        question.answers = answers
        question.multi_choice = multi_choice

    def __str__(question):
        return f"(Question contents={question.contents}, answers={len(question.answers)}, multi_choice={question.multi_choice})"

def question_unwrap(question):
    assert type(question) is FeedBuzzQuestion, "question_unwrap failed assertion"

def question_marked(question):
    question_unwrap(question)

    for answer in question.answers:
        answer_unwrap(answer)
        return True

    return False

class FeedBuzzScoreRange:
    def __init__(scorerange, at=-1, description=""):
        scorerange.at = at
        scorerange.description = ""

    def __str__(scorerange):
        return f"(ScoreRange at={scorerange.at}, description={scorerange.description})"

def scorerange_unwrap(scorerange):
    assert type(scorerange) is FeedBuzzScoreRange, "scorerange_unwrap failed assertion"

class FeedBuzzTest:
    def __init__(test, time_limit=0, title="", description="", questions=None, ranges=None, maximum_possible=0, sparing=True):
        if questions is None:
            questions = []

        if ranges is None:
            ranges = []

        test.title = ""
        test.time_limit = 0
        test.description = ""
        test.questions = questions
        test.ranges = ranges
        test.maximum_possible = 0
        test.sparing = sparing

    def __str__(test):
        return f"(Test title={test.title}, time_limit=test.time_limit)"

def test_unwrap(test):
    assert type(test) is FeedBuzzTest, "test_unwrap failed assertion"

def __test_sort_range(set_check):
    def sorter(scorerange):
        if scorerange.at in set_check:
            original = set_check[scorerange.at]
            raise FeedBuzzException(f"Score range (position {scorerange.at}) is first defined: '{original.description}'")

        scorerange_unwrap(scorerange)
        set_check[scorerange.at] = scorerange
        return scorerange.at

    return sorter

def test_sort_ranges(test):
    test_unwrap(test)
    set_check = dict()

    # If a key function is given, apply it once to each list item and sort them, ...
    test.ranges.sort(key=__test_sort_range(set_check))

def test_score_description(test, score=0):
    test_unwrap(test)
    # NOTE: this is assuming if test.ranges are sorted!

    for scorerange in reversed(test.ranges):
        if score >= scorerange.at:
            return scorerange.description

    return ""

def test_check_validity(test):
    test_unwrap(test)

    if not test.questions:
        raise FeedBuzzException("Test has no questions.")

    for idx, question in enumerate(test.questions):
        if not question.answers:
            raise FeedBuzzException(f"Question #{idx+1} '{question.contents}' has no answers, provide an answer to this question.")

    for idx, scorerange in enumerate(test.ranges):
        if scorerange.at < 0:
            raise FeedBuzzException(f"Score Range #{idx+1} '{scorerange.description}' has no defined place.")

class FeedBuzzPlayer:
    def __init__(player, test=None, score=0, time_start=datetime_now(), current=0):
        if test is None:
            raise FeedBuzzException("FeedBuzzPlayer.test is none")
        
        questions = test.questions
        ranges = test.ranges

        player.time_start = datetime_now()
        player.time_finished = player.time_start
        player.questions = test.questions
        player.ranges = test.ranges
        player.score = 0
        player.current = 0

def player_unwrap(player):
    assert type(player) is FeedBuzzPlayer, "player_unwrap failed assertion"

def player_time_taken(player):
    player_unwrap(player)
    return player.time_finished - player.time_start

def player_is_overdue(test, player):
    test_unwrap(test)
    player_unwrap(player)

    test_time_limit = timedelta(seconds=test.time_limit)
    time_taken = player_time_taken(player)

    return (player.questions and time_taken > test_time_limit, time_taken -test_time_limit)

def player_is_finished(player):
    player_unwrap(player)
    return player.questions and player.current >= len(player.questions)

def player_start_test(player):
    player_unwrap(player)

    player.current = 0
    player.score = 0
    player.time_start = datetime_now()

def player_calculate_score(test, player):
    test_unwrap(test)
    player_unwrap(player)

    score = 0

    for question in test.questions:
        multi_choice = question.multi_choice
        question_score = 0

        for answer in question.answers:
            if not answer.toggled:
                continue

            if multi_choice:
                question_score = max(question_score + answer.score, 0)
            else:
                question_score += answer.score

        score = max(score + question_score, 0)

    return score

def test_calculate_maximum(test):
    test_unwrap(test)
    
    maximum = 0

    for question in test.questions:
        multi_choice = question.multi_choice
        question_maximum = 0

        for answer in question.answers:
            if answer.score < 0:
                continue

            if multi_choice:
                question_maximum += answer.score
            else:
                question_maximum = max(question_maximum, answer.score)

        maximum += question_maximum

    return maximum

from os import get_terminal_size

def encode_seconds(seconds):
    seconds = int(seconds)
    string = f"{seconds%60}s"

    if seconds >= 60:
        string = f"{(seconds//60)%60}m{string}"

    if seconds >= 3600:
        string = f"{(seconds//60//60)%60}h{string}"

    return string

def terminal_size():
    return get_terminal_size()

def terminal_block(symbol):
    size = terminal_size()
    print(symbol * size.columns, end="")

def terminal_bold(string):
    print(f"\033[1m{string}\033[0m", end="")

def terminal_italic(string):
    print(f"\033[3m{string}\033[0m", end="")

def terminal_marked(string):
    print(f"\033[7m{string}\033[0m", end="")

def clear_screen():
    # https://en.wikipedia.org/wiki/ANSI_escape_code#Control_Sequence_Introducer_commands
    print("\033[H\033[J", end="")

def terminal_keyword_input(question, choices, label="select"):
    # [(keyword, question)]
    keywords = set(choice[0] for choice in choices)
    terminal_marked("  ")
    terminal_italic(" " + question)
    print()

    try:
        while True:
            for choice in choices:
                keyword, description = choice
                terminal_bold(keyword.rjust(10))
                print(" " + str(description))

            terminal_italic(f"[{label}]: ")
            answer = input().strip().lower()

            if not answer:
                continue

            if answer not in keywords:
                print("Not in keywords, try again.")
                continue

            return answer
    except KeyboardInterrupt:
        terminal_marked(" interrupt detected ")
        return None

def player_start_anticipation(test):
    clear_screen()

    terminal_block("-")
    print("\r--- Feedbuzz ")
    terminal_marked("  ")
    terminal_bold(f" {test.title}")
    print("\n")
    
    print(test.description)
    print()

    terminal_italic("Questions: ")
    terminal_bold(str(len(test.questions)))

    if test.time_limit > 0:
        print()
        terminal_italic("Time Limit: ")
        terminal_bold(encode_seconds(test.time_limit))

    print()
    terminal_block("-")
    print()

    if terminal_keyword_input("Select a keyword:", (
                ("begin", "Begin"),
                ("quit", "Quit and return to terminal"),
            )) == "begin":
        clear_screen()
        print("\n")
        return True
    
    return False
    
def player_display_question(idx, question):
    question_unwrap(question)

    answers = question.answers
    contents = question.contents
    multi_choice = question.multi_choice

    terminal_marked(" ")
    terminal_bold(f"{idx+1}. ".rjust(4))
    terminal_bold(" " + contents)
    print()

    if multi_choice:
        terminal_italic("      (multiple-choice)")
        print()

    for idx, answer in enumerate(answers):
        if answer.toggled:
            terminal_marked(f"{idx+1}.".rjust(5))
        else:
            print(f"{idx+1}.".rjust(5), end="")

        print(" ", end="")
        print(answer.contents)

    terminal_italic("Pick or erase with an answer number. Type 'done' if you are done answering.")
    print()

def player_finish_test(test, player):
    player.time_finished = datetime_now()
    player.score = player_calculate_score(test, player)

def player_show_statistics(test, player):
    test_unwrap(test)
    player_unwrap(player)

    clear_screen()
    print()
    terminal_marked("     ")
    terminal_bold(" Finished!")
    print()
    print()

    overdue, off_delta = player_is_overdue(test, player)

    if overdue:
        time_taken = player_time_taken(player)

        print("  ", end="")
        terminal_marked(" OVERDUE ")
        print(f" by {off_delta.seconds} second(s).")

    terminal_bold("Score: ")
    print(f"{player.score}")

    terminal_italic(test_score_description(test, player.score))
    print()

    # TODO: remind player of score and time, that's all!

def player_confront(test, player):
    player_unwrap(player)

    current = player.current

    try:
        question = player.questions[current]
        multi_choice = question.multi_choice
        answers = question.answers
    except IndexError:
        player_finish_test(test, player)
        player_show_statistics(test, player)
        return False

    while True:
        try:
            player_display_question(current, question)
            answer_input = input("Your answer: ").strip().lower()

            if answer_input == "done":
                if not question_marked(question):
                    print("No answers selected.")
                    pass

                player.current += 1
                return True

            try:
                answer_idx = int(answer_input)
            except ValueError:
                print("Not a number.")
                continue

            if answer_idx <= 0:
                print("Answer number exceeds below 1, type blank to see the question again.")
                continue

            if answer_idx > len(answers):
                print(f"Answer number exceeds above {len(answers)}, type blank to see the question again.")
                continue

            answer = answers[answer_idx - 1]

            if multi_choice:
                answer.toggled = not answer.toggled
            else:
                # NOTE: lazy way
                for question_answer in answers:
                    question_answer.toggled = False
                answer.toggled = True
        except KeyboardInterrupt:
            return False

    return False

def datetime_json(date):
    return date.strftime("%Y-%m-%dT%H:%M:%S.%f")

def test_results_json(test, player):
    test_unwrap(test)
    player_unwrap(player)

    score_description = test_score_description(test, player.score)

    metadata = dict(name=test.title, description=test.description, time_limit=test.time_limit)
    time = dict(started=datetime_json(player.time_start), finished=datetime_json(player.time_finished))
    performance = dict(score=player.score, maximum=test.maximum_possible, score_description=score_description)
    questions_json = []

    for question in test.questions:
        answers_json = []
        question_json = dict(answers=answers_json)

        for answer in question.answers:
            answer_json = dict(score=answer.score, picked=answer.toggled)
            answers_json.append(answer_json)

        questions_json.append(question_json)

    return dict(metadata=metadata, time=time, performance=performance, questions=questions_json)
