# Task 3 — Variables and constants

The rate settings in `milkrate.py` use uppercase names to mark them as constants by convention. Python still allows reassignment, so the convention helps readers avoid accidental edits. Valid identifiers contain letters, digits and underscores but cannot start with a digit or be a keyword.

Run `python -m Task03.constants_demo` from the project root to view the rate constants, demonstrate dynamic types, and swap two values with multiple assignment. Repeating literal rates across many functions would make updates inconsistent; named values centralise the settings. Rate calculation uses a fixed number of operations, so its time and auxiliary space are O(1).
