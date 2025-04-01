from datetime import datetime
datetime_now = datetime.now

class FeedBuzzException(Exception):
    pass

class FeedBuzzAnswer:
    def __init__(answer, contents="", description="", score=0):
        answer.contents = contents
        answer.description = ""
        answer.score = 0

class FeedBuzzQuestion:
    def __init__(question, contents="", answers=None, multi_choice=False):
        if answers is None:
            answers = []

        question.contents = contents
        question.answers = answers
        question.multi_choice = multi_choice

    def __str__(question):
        return f"(Question name={question.name}, time_limit=test.time_limit)"

class FeedBuzzTest:
    def __init__(test, time_limit=0, name="", description="", questions=None, ranges=None):
        if questions is None:
            questions = []

        if ranges is None:
            ranges = []

        test.name = ""
        test.time_limit = 0
        test.description = ""
        test.questions = questions
        test.ranges = ranges

    def __str__(test):
        return f"(Test name={test.name}, time_limit=test.time_limit)"

def test_unwrap(test):
    assert type(test) is FeedBuzzTest, "test_unwrap failed assertion"

def test_check_validity(test):
    test_unwrap(test)

    if not test.questions:
        raise FeedBuzzException("Test has no questions.")

    for idx, question in enumerate(test.questions):
        if not question.answers:
            raise FeedBuzzException(f"Question #{idx+1} '{question.contents}' has no answers, provide an answer to this question.")

class FeedBuzzPlayer:
    def __init__(player, test=None, score=0, time_start=datetime_now()):
        if test is None:
            raise FeedBuzzException("FeedBuzzPlayer.test is none")
        
        questions = test.questions
        ranges = test.ranges

        player.time_start = datetime_now()
        player.score = 0
        player.questions = test.questions
        player.ranges = test.ranges
        player.current = None

def player_unwrap(player):
    assert type(player) is FeedBuzzPlayer, "player_unwrap failed assertion"

def player_start_test(player):
    player_unwrap(player)

    player.current = iter(player.questions)
    player.score = 0
    player.time_start = datetime_now()
