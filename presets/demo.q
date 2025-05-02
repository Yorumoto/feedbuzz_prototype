# 'demo.q'
# Date: April 4, 2025
# Author: Arric Light

# This is to showcase the features of a typical .q (FeedBuzz Lingo) file.

Test:
    Title "This is the title"
    Description "This is the description to instruct and elaborate."

    TimeLimit 30;

    # don't forget the last attribute must end with a semicolon!

Scoring:
    At 15 "You scored the topmost!"
    At 10 "You at least scored 10 to 14"
    At 5 "You at least scored 5"
    At 0 "You scored below 5";

Question "Single choice question":
    Choice Single
    Answer "Wrong answer -5" Loss 5
    Answer "Right answer +1" Gain 1
    Answer "Wrong answer -5" Loss 5
    Answer "Right answer +10" Gain 10;

Question "Multiple choice question":
    Choice Multiple
    Answer "Wrong answer -5" Loss 5
    Answer "Right answer +1" Gain 1
    Answer "Wrong answer -5" Loss 5
    Answer "Right answer +10" Gain 10;
