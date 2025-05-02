# 'grit.q'
# Date: April 4, 2025
# Author: Arric Light
#
# Original from 'Grit' by Angela Duckworth
#

Test:
    Title "The Grit Scale"
    TimeLimit 0 # no time limit
    Description "The Grit Scale implemented in FeedBuzz.\n\nThe Grit Scale by Angela Duckworth. Scoring segregation labels are made up."
    Deduction Sparing
    ;

Scoring:
    At 50 "Extremely gritty"
    At 40 "Very gritty"
    At 30 "Moderately gritty"
    At 20 "Quite gritty"
    At 10 "Not at all gritty"
    At 0 "???? gritty"
    ;

Question "New ideas and projects sometimes distract me from previous ones.":
    Answer "Very much like me." Gain 1
    Answer "Mostly like me." Gain 2
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 4
    Answer "Not at all like me." Gain 5
    ;

Question "Setbacks don't discourage me. I don't give up easily.":
    Answer "Very much like me." Gain 5
    Answer "Mostly like me." Gain 4
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 2
    Answer "Not at all like me." Gain 1
    ;

Question "I often set a goal but later choose to pursue a different one.":
    Answer "Very much like me." Gain 1
    Answer "Mostly like me." Gain 2
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 4
    Answer "Not at all like me." Gain 5
    ;

Question "I am a hard worker.":
    Answer "Very much like me." Gain 5
    Answer "Mostly like me." Gain 4
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 2
    Answer "Not at all like me." Gain 1
    ;

Question "I have difficulty maintaining my focus on projects that take more than a few months to complete.":
    Answer "Very much like me." Gain 1
    Answer "Mostly like me." Gain 2
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 4
    Answer "Not at all like me." Gain 5
    ;

Question "I finish whatever I begin.":
    Answer "Very much like me." Gain 5
    Answer "Mostly like me." Gain 4
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 2
    Answer "Not at all like me." Gain 1
    ;

Question "My interests change from year to year.":
    Answer "Very much like me." Gain 1
    Answer "Mostly like me." Gain 2
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 4
    Answer "Not at all like me." Gain 5
    ;
    
Question "I am diligent. I never give up.":
    Answer "Very much like me." Gain 5
    Answer "Mostly like me." Gain 4
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 2
    Answer "Not at all like me." Gain 1
    ;

Question "I have been obsessed with a certain idea or project for a short time but later lost interest.":
    Answer "Very much like me." Gain 1
    Answer "Mostly like me." Gain 2
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 4
    Answer "Not at all like me." Gain 5
    ;

Question "I have overcome setbacks to conquer an important challenge.":
    Answer "Very much like me." Gain 5
    Answer "Mostly like me." Gain 4
    Answer "Somewhat like me." Gain 3
    Answer "Not much like me." Gain 2
    Answer "Not at all like me." Gain 1
    ;
