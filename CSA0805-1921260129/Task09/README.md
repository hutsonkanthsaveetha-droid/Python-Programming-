# Task 9 — Implementation and tests

Run the interactive calculator with `python -m Task09.calculator`. Run automated tests from the project root with `python -m unittest Task09/test_calculator.py`.

Expected test cases include:
- Standard: 10 L, fat 3.5, SNF 8.5 → rate ₹30.00, payment ₹300.00.
- Above: 8.5 L, fat 4.2, SNF 8.7 → rate ₹33.40, payment ₹283.90.
- Below: 12 L, fat 3.1, SNF 8.3 → rate ₹27.80, payment ₹333.60.
- Fat boundaries 2.0 and 7.0 accepted; 1.9 and 7.1 rejected.
- Negative litres, nonnumeric text, blank ID, invalid shift rejected.
Capture the actual unittest output as evidence. Automated tests are repeatable and take about O(m) time for m test cases; manual retesting also takes O(m) human actions and is slower and more error-prone after each change.
