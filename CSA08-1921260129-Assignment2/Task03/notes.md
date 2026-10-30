# Q3 - Vehicle Registration Validator

`normalise` removes spaces and hyphens and converts to uppercase. `is_valid` checks 2 state letters, 2 district digits, 1-2 series letters and 4 final digits by slicing; no regular expressions are used in the required implementation. `format_receipt` prints four groups.

Strings are immutable: `upper()` returns a new string and does not modify the original. For a 9-character value `s[-4:]` returns the last four characters and `s[4:-4]` returns one series character; for a 10-character value, the middle slice returns two characters.

Alternative: `re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg)` is concise. Both approaches take O(L) time; slicing exposes each component, while regex is compact for more complex patterns.
