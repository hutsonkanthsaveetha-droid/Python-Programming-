# Task 4 — Expressions

For nearest 0.1 percentage-point steps:
`fat_steps = round((fat - 3.5) / 0.1)` and `snf_steps = round((snf - 8.5) / 0.1)`.
Then `rate = 30.00 + fat_steps*0.40 + snf_steps*0.30`; `amount = litres*rate`. For production monetary calculations use `Decimal` and an explicit rounding mode, as in `milkrate.py`.

Unexpected examples:
1. `(4.2-3.5)/0.1` may be `7.000000000000001` due to binary floating point.
2. `0.1+0.2 == 0.3` is `False` for the same reason.
3. `round(2.675, 2)` can give `2.67` because the stored float is slightly below the decimal value and Python uses ties-to-even where a tie is exact.
`round()` chooses a nearby integer (ties-to-even); `int()` truncates toward zero; `math.floor()` rounds down toward negative infinity. For fat=4.2, raw step count is near 7 and all three produce 7. For fat=3.1, raw count is near -4: `round` gives -4, `int` gives -3, and `floor` gives -4. Thus using `int` would incorrectly reduce the magnitude of a negative adjustment. Operator precedence means multiplication is evaluated before addition; parentheses should make intended grouping explicit. `**` is exponentiation and binds more tightly than unary minus, so `-2**2 == -4`, whereas `(-2)**2 == 4`. Chained comparison `2.0 <= fat <= 7.0` checks both bounds; `and`/`or` combine Boolean conditions. Each arithmetic method is O(1) time and O(1) auxiliary space.
