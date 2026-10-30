# Q7 - Diagnose, Redesign and Validate

The selected bottleneck is Q6 plain recursion. It recomputes the same lower stair counts in multiple branches, so recursive calls grow exponentially. Objective: preserve exact answers while reducing work to one pass and supporting n=1000 without recursion depth failure.

Redesign: use two variables for the previous two counts and update them in a loop. This removes repeated calls and uses constant auxiliary space. Q7 compares both versions on n=20,25,30 and separately runs the iterative design for n=1000. Raw results are saved in `data/q7_raw_comparison.csv`.

Prediction: the iterative solution will return identical values with n-1 update steps and far fewer operations; original recursion remains useful only as a small-input teaching example.
