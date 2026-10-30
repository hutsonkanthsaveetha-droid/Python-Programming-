# Q6 - Recursion and Its Limits

The recurrence is W(n)=W(n-1)+W(n-2), with W(0)=W(1)=1. Plain recursion repeats subproblems; memoisation stores each result once. The output includes answers for n=1..6, the full n=5 call tree in `Task06/call_tree_n5.txt`, naive and memoised function-call counts for n=10,20,25,30, and attempts to run both recursive versions at n=1000. The default recursion limit causes `RecursionError` before a 1,000-deep recursive call completes.

Complexity: naive recursion O(phi^n) time and O(n) call stack; memoised recursion O(n) time and O(n) cache plus stack; iterative two-value DP O(n) time and O(1) auxiliary space. Increasing recursion limit risks exhausting the C/Python stack; iterative DP is the deployment choice for n=1000.
