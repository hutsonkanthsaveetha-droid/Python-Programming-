# Task 2 — Interpreter values and types

Interactive evidence to run and screenshot:

```pycon
>>> type(10)
<class 'int'>
>>> type(10.0)
<class 'float'>
>>> type("10")
<class 'str'>
>>> type(True)
<class 'bool'>
>>> type([10, 8.5])
<class 'list'>
>>> 7 / 2
3.5
>>> 7 // 2
3
>>> 7 % 2
1
>>> -7 // 2
-4
>>> 0.1 + 0.2 == 0.3
False
```

`/` gives true division; `//` floors toward negative infinity (so -7//2 is -4); `%` gives the remainder consistent with floor division. Binary floats cannot represent many decimal fractions exactly, so 0.1+0.2 is a nearby approximation rather than exactly 0.3. `Decimal("0.1")` preserves the decimal input; `Decimal(float("0.1"))` imports the float's binary approximation and therefore shows many extra digits.

Use integer paise when all amounts are guaranteed to be whole paise; use `Decimal` for decimal monetary calculations. `round()` on float does not make all intermediate binary arithmetic exact. Time to sum n amounts is O(n) for all three approaches; accumulator space is O(1), excluding input storage. Use `sys.getsizeof(value)` to measure implementation-specific object size on your own interpreter.
