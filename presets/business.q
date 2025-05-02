# 'business.q'
# Date: April 4, 2025
# Author: Arric Light

Test:
    Title "Are You a Good Entrepreneur?"
    Description "This test will estimate if you are well onto becoming an entrepreneur, be honest with your mentality.\n\nInstructions: Choose one answer per question, points are awarded or deducted based on your selection\n(Generated from DeepSeek)"
    TimeLimit 120
    Deduction Sparing
    ;

Scoring:
    At 15 "You have a strong mindset. You are resilient and creative and you calculate risks."
    At 8 "You have some strengths, but you still have room for growth."
    At 0 "You have a mindset to work on. You have aversions of risk and tendencies to react, you might struggle with uncertainty and fail with persistence."
    ;

Question "When faced with a failed project, you:":
    Choice Single
    Answer "Give up and move to a safer career path." Loss 2
    Answer "Analyze what went wrong and try again with adjustments." Gain 3
    Answer "Blame external factors and avoid responsibility." Loss 3
    Answer "Immediately pivot to a completely new idea without reflection." Gain 3
    ;

Question "How do you approach risks?":
    Choice Single
    Answer "Avoid risks at all cost-safety first." Loss 2
    Answer "Take calculate risks after research and planning." Gain 4
    Answer "Dive into high-risk opportunities without much thought." Loss 1
    Answer "Prefer moderate risks but hesitate without guarantees." Gain 1;

Question "Your idea is criticized by an expert. You:":
    Choice Single
    Answer "Ditch the idea immediately." Loss 3
    Answer "Refine the idea based on feedback while keeping your vision." Gain 3
    Answer "Defend it aggressively without considering feedback." Loss 2
    Answer "Seek a second opinion before deciding." Gain 1
    ;

Question "When resources are tight:":
    Choice Single
    Answer "Panic and cut costs immediately." Loss 2
    Answer "Get creative-barrier, negotiate, and find low-cost solutions." Gain 4
    Answer "Wait for external funding before acting." Loss 1
    Answer "Reduce ambitions to match available resources." Gain 2;

Question "Your primary motivation to start a business is:":
    Choice Single
    Answer "Money and financial freedom." Gain 1
    Answer "Solving a problem you are passionate about." Gain 4
    Answer "Following a trend or copying others." Loss 2
    Answer "Escaping a 9-to-5 job but with no clear plan." Loss 1
    ;
