# Task 7 — Module

`import milkrate` uses names as `milkrate.payout`; `from milkrate import payout` imports the selected name directly; `import milkrate as mr` uses an alias. Python searches locations in `sys.path`, including the script/current working directory and installed library directories. `math` and `decimal` are standard-library modules.

The guard must be exactly `if __name__ == "__main__":`. When a file is run directly, its `__name__` is `"__main__"` and its demo executes. When imported, `__name__` is `"milkrate"`, so the demo table does not print. Without the guard, demo output would occur on import. Python caches imported modules in `sys.modules`, avoiding repeated full execution during the same process. Copying functions into many scripts means each copy must be updated when rates change; a shared module has one source of truth.

Run from the project root with `python -m Task07.test_import` so the project root is on Python's module search path.
