# Q5 - Functions, Parameters and Scope

A mutable default list is created once at function definition time and reused. `order=None` creates a fresh list for each call. The program prints `add_item_buggy.__defaults__` after calls, demonstrates three separate customer orders, positional/keyword/default arguments, a tuple return of total and GST, and local/global/nonlocal scope.

Changing a module-level name inside a function requires `global`; it is usually avoided because it hides data flow and makes tests harder. A closure can retain private state with `nonlocal`. If the caller always passes a list, the list is explicit; per customer, list storage is O(m) for m items and append is amortised O(1).
