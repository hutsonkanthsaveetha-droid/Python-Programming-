# Q2 - OTP Attempts

Both loop forms count only non-blank entries. `continue` skips blank input inside an inner prompt loop, `break` exits the attempt loop on a correct OTP, `pass` marks a no-op failure hook, and loop `else` executes only when all counted attempts finish without `break`. A while loop fits changing attempt limits; a for loop fits a fixed count. Incrementing before checking for blank input wrongly consumes an attempt; failing to increment can create an infinite loop.

The security-question rule sets the limit to five when the answer is correct, otherwise three. Recursive alternative: call the function for the next entry and remaining attempts; time O(a), stack O(a), compared with O(a) time and O(1) auxiliary space for loops.
