Test:
    Title "BasicFileReading"
    Description ""
    TimeLimit -10;

Question "What is one plus one?":
    Choice Single
    Answer "Two." Loss 10
    Answer "One." Gain 0;

Question "What is the meaning of life?":
    Choice Single
    Answer "I don't know." Gain 10
    Answer "42." Loss 10;
