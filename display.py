from curses import newpad
from curses import A_BLINK, A_BOLD, A_DIM, A_UNDERLINE, A_ITALIC, A_REVERSE, A_ALTCHARSET
from curses import init_pair, use_default_colors, start_color, has_colors, color_pair, can_change_color, init_color
from curses import COLOR_BLUE, COLOR_RED, COLOR_YELLOW, COLOR_GREEN, COLOR_WHITE, COLOR_BLACK, COLOR_CYAN
from curses import error as curses_error
from curses import noecho, cbreak, curs_set
from curses.textpad import rectangle
from curses import is_term_resized
from sys import stderr

PAIR_SELECTION = 1
PAIR_TITLE = 2
PAIR_PAPER = 3
PAIR_SELECTION_NOT = 4

CODENAME = "feedbuzz.display"

def words(string):
    # NOTE: stored in memory
    return string.split(" ")

def encode_seconds(seconds):
    seconds = int(seconds)
    string = f"{seconds%60}s"

    if seconds >= 60:
        string = f"{(seconds//60)%60}m{string}"

    if seconds >= 3600:
        string = f"{(seconds//60//60)%60}h{string}"

    return string

class FeedBuzzChoiceState:
    def __init__(state, choice=0, choices=None, select_attrib=0, nonselect_attrib=0):
        if choices is None:
            choices = []

        state.choice = choice
        state.choices = choices
        state.select_attrib = select_attrib
        state.nonselect_attrib = nonselect_attrib

def feedbuzz_display_setup(window):
    noecho()
    cbreak()

    window.keypad(True)

    start_color()


    try:
        use_default_colors()
    except curses_error:
        print(f"{CODENAME}: use_background_colors failed!", file=stderr)

    try:
        init_pair(PAIR_SELECTION_NOT, COLOR_BLUE, COLOR_BLACK)
        init_pair(PAIR_TITLE, COLOR_BLACK, COLOR_CYAN)
        init_pair(PAIR_PAPER, COLOR_BLACK, COLOR_WHITE)
        init_pair(PAIR_SELECTION, COLOR_BLACK, COLOR_BLUE)
    except curses_error as e:
        print(f"{CODENAME}: init_pair failed!", file=stderr)


def size(window):
    return window.getmaxyx()

def center(window):
    height, width = size(window)
    return (height>>1, width>>1)

EMPTY = " "

def fill_rectangle(window, ay, ax, by, bx, attribs):
    height, width = size(window)

    for y in range(max(ay, 0), min(by+1, height)):
        for x in range(max(ax, 0), min(bx+1, width)):
            window.addch(y, x, EMPTY, attribs)

def cram_text(window, y, x, height, width, text, attribs):
    try:
        dx = 0
        dy = 0

        for word in words(text):
            if dx+len(word) > width:
                dx = 0
                dy += 1

                if dy > height:
                    return

            for character in word:
                if character == "\r":
                    dx = 0
                    continue
                if character == "\n":
                    dy += 1

                    if dy > height:
                        return

                    dx = 0
                    continue

                window.addch(y + dy, x + dx, character, attribs)
                dx += 1

                if dx > width:
                    dx = 0
                    dy += 1

                    if dy > height:
                        return

            dx += 1

            if dx > width:
                dx = 0
                dy += 1

                if dy > height:
                    return
    except StopIteration:
        pass

def choice_state_draw(window, state, y, x, width):
    choices = state.choices
    nonselect_attrib = state.nonselect_attrib
    select_attrib = state.select_attrib
    selected = state.choice

    for idx, choice in enumerate(choices):
        attrib = select_attrib if idx == selected else nonselect_attrib
        fill_rectangle(window, y, x, y, x+width, attrib)
        window.addstr(y, x, choice[:width], attrib)
        y += 1

from curses import KEY_ENTER, KEY_UP, KEY_DOWN, KEY_EOL

def choice_state_getch(window, state):
    try:
        ch = window.getch()

        if ch == KEY_ENTER or ch == 10 or ch == 13:
            return state.choice
        elif ch == KEY_EOL:
            return state.choice
        elif ch == KEY_UP:
            state.choice = (state.choice - 1) % len(state.choices)
        elif ch == KEY_DOWN:
            state.choice = (state.choice + 1) % len(state.choices)

        return
    except KeyboardInterrupt:
        return

def refresh_test_beginning(window, test):
    scy, cx = center(window)
    cy = scy
    cx -= 20
    cy -= 10

    fill_rectangle(window, cy, cx, cy, cx+40, color_pair(PAIR_TITLE))
    window.addstr(cy, cx+1, "FeedBuzz", color_pair(PAIR_TITLE) | A_REVERSE)
    cy += 1

    attribs = color_pair(PAIR_PAPER)

    fill_rectangle(window, cy, cx, cy+12, cx+40, attribs)

    if not test.title:
        window.addstr(cy+1, cx+1, "(Untitled Test)", attribs | A_BOLD)
    else:
        window.addstr(cy+1, cx+1, test.title[:38], attribs | A_BOLD)

    cy += 1

    if test.time_limit > 0:
        window.addstr(cy+1, cx+1, f"Time limit: {encode_seconds(test.time_limit)}", attribs)

    cy += 1
    window.addstr(cy+1, cx+1, f"Questions: {len(test.questions)}", attribs | A_UNDERLINE)
    cy += 2

    cram_text(window, cy+1, cx+1, 7, 38, test.description, attribs)

    window.addstr(cy+13, cx+1, "Press the up and down keys to move")
    window.addstr(cy+14, cx+1, "Press the enter key to select")

    return cx, cy


def feedbuzz_display_test_beginning(window, test):
    choice_state = FeedBuzzChoiceState(choice=0, choices=[
            "Begin test",
            "Quit"
        ], nonselect_attrib=color_pair(PAIR_SELECTION_NOT), select_attrib=color_pair(PAIR_SELECTION))

    while True:
        window.clear()
        cx, cy = refresh_test_beginning(window, test)
        window.addstr(0, 0, f"size: {size(window)}")
        choice_state_draw(window, choice_state, cy+10, cx, 40)

        window.move(0, 0)
        window.refresh()

        choice = choice_state_getch(window, choice_state)

        if choice is not None:
            return choice

def feedbuzz_display_freeze(window):
    window.getch()

