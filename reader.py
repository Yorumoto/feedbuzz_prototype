from test import FeedBuzzQuestion, FeedBuzzAnswer

def __breakpoint():
    raise SystemExit("(program breakpoint)")

class ReaderSyntaxError(Exception):
    pass

def reader_error(state, error_message):
    lineno = state.lineno

    message = f"line {lineno+1}: {error_message}"
    return ReaderSyntaxError(message)

class ReaderState:
    def __init__(state):
        # for convenience to make the reading flow seamless
        # instead of having to go back by one character.
        state.last_character = ""
        state.test_line = -1
        state.lineno = 0

def character_is_newline(char):
    # windows applications for micr0$*ft
    if char == "\r":
        return True
    elif char == " ":
        return True
    elif char == "\n":
        return True

    return False

def reader_count_newline(state, char):
    # windows applications for micr0$*ft
    if char == "\r":
        # print(f"reader_count_newline: <carriage return>")
        return True
    elif char == " ":
        # print(f"reader_count_newline: <space>")
        return True
    elif char == "\n":
        state.lineno += 1
        # print(f"reader_count_newline: <newline>")
        return True

    # print(f"reader_count_newline: (char) {char}")

    return False

def reader_hand_character(state, char):
    if char == "\n":
        return

    state.last_character = char

SUDDEN_EOF_MESSAGE = "End-of-file reached abruptly"

def read_char_file_safe(state, file, bypass=False):
    if state.last_character:
        char = state.last_character
        state.last_character = ""
    else:
        char = file.read(1)

    if not bypass and not char:
        raise reader_error(state, SUDDEN_EOF_MESSAGE)
        return ""

    return char

def read_char_safe(state, file, bypass=False, skip_whitespace=False):
    char = read_char_file_safe(state, file, bypass)

    if reader_count_newline(state, char) and skip_whitespace:
        while True:
            char = read_char_file_safe(state, file, bypass)

            if not reader_count_newline(state, char):
                return char

    return char

def identifier_is_valid(char):
    return char.isalpha()

def identifier_is_keyword(keyword):
    # NOTE: lazy way of is_capitalized(word)
    return keyword == (keyword[0].capitalize() + keyword[1:])

def identifier_read(state, file, startchar):
    identifier = ""
    identifier += startchar

    while True:
        char = read_char_safe(state, file)

        if not identifier_is_valid(char):
            reader_hand_character(state, char)
            return identifier

        identifier += char

    return identifier

def reader_check_unexpected_characters(state, char):
    raise reader_error(state, f"Unexpected character: ({ord(char)}) {char}")

def reader_read_string(state, file, process_name=""):
    quote_char = read_char_safe(state, file, skip_whitespace=True)

    if quote_char != "'" and quote_char != '"':
        raise reader_error(state, f"({process_name}) Expected a string, got: '{quote_char}'")

    char = read_char_safe(state, file)
    string = ""
    backslashed = False

    while char != quote_char or backslashed:
        if backslashed:
            if char == "n":
                string += "\n"
            elif char == "r":
                string += "\r"
            elif char == "'":
                string += "'"
            elif char == "\"":
                string += "\""
            else:
                raise reader_error(state, f"({process_name}) Unknown backslashed character: \\{char}")

            backslashed = False
            char = ""
        elif not backslashed and char == "\\":
            backslashed = True
        elif char != "\r":
            string += char

        char = read_char_safe(state, file)

        if char == "\n":
            raise reader_error(state, f"({process_name}) Newlines are not allowed in a string!")

    print(string)

    return string

def character_is_numerical(character):
    return character.isnumeric()

def reader_read_integer(state, file, process_name="", positive_only=False):
    # NOTE: this is assuming this computer follows the ASCII standard
    #       too many standards in this world for one person

    char = read_char_safe(state, file, skip_whitespace=True)

    if positive_only and char == "-":
        raise reader_error(state, f"({process_name}) Expected a positive number, got a negative sign.")

    if not character_is_numerical(char):
        raise reader_error(state, f"({process_name}) Expected a number, got: '{char}'")

    value = 0
    negate = char == '-'

    START_CHAR = ord('0')

    while True:
        digit = ord(char) - START_CHAR
        value = (value*10) + digit
        char = read_char_safe(state, file)
        
        if not character_is_numerical(char):
            reader_hand_character(state, char)
            break

    if negate:
        value = -value

    return value

# literally a colon after a 'Test' or a 'Question' keyword
def reader_signify_data_container(state, file, keyword=""):
    char = read_char_safe(state, file)

    if char != ":":
        raise reader_error(state, f"':' expected after '{keyword}'")

def reader_read_test(test, state, file):
    reader_signify_data_container(state, file, "Test")

    while True:
        char = read_char_safe(state, file, skip_whitespace=True)

        if char == ";":
            return

        if identifier_is_valid(char):
            keyword = identifier_read(state, file, char)

            if keyword == "Name":
                name = reader_read_string(state, file, "Test.Name")
                test.name = name
            elif keyword == "Description":
                description = reader_read_string(state, file, "Test.Description")
                test.description = description
            elif keyword == "TimeLimit":
                time_limit = reader_read_integer(state, file, "Test.TimeLimit", positive_only=True)
                test.time_limit = time_limit
            else:
                raise reader_error(state, f"Unknown keyword in Test entry: '{keyword}'")
        else:
            reader_check_unexpected_characters(state, char)


def reader_read_question(question, state, file, question_contents):
    answers = question.answers
    answer = None

    while True:
        char = read_char_safe(state, file, skip_whitespace=True)

        if char == ";":
            return

        if identifier_is_valid(char):
            keyword = identifier_read(state, file, char)

            if keyword == "Choice":
                firstchar = read_char_safe(state, file, skip_whitespace=True)

                if not identifier_is_valid(firstchar):
                    raise reader_error(state, f"(Question.Choice) 'Single' or 'Multi' keyword expected")

                value_keyword = identifier_read(state, file, firstchar)

                if value_keyword == "Single":
                    question.multi_choice = False
                elif value_keyword == "Multi":
                    question.multi_choice = True
                else:
                    raise reader_error(state, f"(Question.Choice) Keyword is not either 'Single' or 'Multi'")
            elif keyword == "Answer":
                answer_contents = reader_read_string(state, file, "Question.Answer")
                answer = FeedBuzzAnswer(contents=answer_contents, description="", score=0)
                answers.append(answer)
            elif keyword == "Gain":
                if answer is None:
                    raise reader_error(state, f"(Question.Answer.Gain) No answer declared yet")

                answer.score = reader_read_integer(state, file, "Question.Answer.Gain", positive_only=True)
            elif keyword == "Loss":
                if answer is None:
                    raise reader_error(state, f"(Question.Answer.Loss) No answer declared yet")

                answer.score = -reader_read_integer(state, file, "Question.Answer.Loss", positive_only=True)
            else:
                raise reader_error(state, f"Unknown keyword in Question entry: '{keyword}'")
        else:
            reader_check_unexpected_characters(state, char)

def reader_read_range(test, state, file):
    while True:
        char = read_char_safe(state, file, skip_whitespace=True)

        if char == ";":
            return

        if identifier_is_valid(char):
            pass
        else:
            reader_check_unexpected_characters(state, char)

def root_nest_identify_keyword(test, state, file, keyword):
    if not identifier_is_keyword(keyword):
        raise reader_error(state, f"Keyword '{keyword}' must be capitalized")

    if keyword == "Question":
        question_contents = reader_read_string(state, file, "Question declaration")
        reader_signify_data_container(state, file, "Question")

        answers = []
        question = FeedBuzzQuestion(contents=question_contents, answers=answers, multi_choice=False)
        reader_read_question(question, state, file, question_contents)
        
        test.questions.append(question)
    elif keyword == "Test":
        if state.test_line >= 0:
            raise reader_error(state, f"Attempted to declare another test entry; test is first declared at line {state.test_line+1}")

        state.test_line = state.lineno
        reader_read_test(test, state, file)
    else:
        raise reader_error(state, f"Unrecognized data entry '{keyword}'; Test, Result, or Question expected.")

def feedbuzz_file_read(test, file):
    state = ReaderState()

    # i'm much of a fan of for(;;) instead of while(1)

    # this is the root parser: looking for
    #
    # Question keyword
    # Test keyword 
    # Result keyword
    while True:
        char = read_char_safe(state, file, bypass=True, skip_whitespace=True)

        if not char:
            # print("- debug: EOF safely")
            return

        if identifier_is_valid(char):
            keyword = identifier_read(state, file, char)
            root_nest_identify_keyword(test, state, file, keyword)
            continue
        
        reader_check_unexpected_characters(state, char)

