def verify_while(entries, correct_otp, max_attempts=3):
    attempts = 0
    iterator = iter(entries)
    verified = False
    while attempts < max_attempts:
        while True:
            try:
                entered = next(iterator)
            except StopIteration:
                return False
            if not entered.strip():
                continue
            break
        attempts += 1
        if entered == correct_otp:
            print(f"Verified after {attempts} counted attempt(s).")
            verified = True
            break
        else:
            pass
    else:
        print("Account locked for 30 minutes.")
    return verified


def verify_for(entries, correct_otp, max_attempts=3):
    iterator = iter(entries)
    verified = False
    for attempt in range(max_attempts):
        while True:
            try:
                entered = next(iterator)
            except StopIteration:
                return False
            if not entered.strip():
                continue
            break
        if entered == correct_otp:
            print(f"Verified after {attempt + 1} counted attempt(s).")
            verified = True
            break
        else:
            pass
    else:
        print("Account locked for 30 minutes.")
    return verified


def verify_with_security(entries, correct_otp, security_answer_ok):
    allowance = 5 if security_answer_ok else 3
    return verify_for(entries, correct_otp, allowance)


def verify_recursive(entries, correct_otp, max_attempts=3, attempts=0, index=0):
    if attempts >= max_attempts:
        print("Account locked for 30 minutes.")
        return False
    if index >= len(entries):
        return False
    entered = entries[index]
    if not entered.strip():
        return verify_recursive(entries, correct_otp, max_attempts, attempts, index + 1)
    if entered == correct_otp:
        print(f"Verified after {attempts + 1} counted attempt(s).")
        return True
    return verify_recursive(entries, correct_otp, max_attempts, attempts + 1, index + 1)


def loop_control_demo():
    print("continue skips blank entries; break exits on success; pass is a no-op failure hook.")


def main():
    print("WHILE LOOP - success")
    verify_while(["", "111111", "123456"], "123456")
    print("WHILE LOOP - lock")
    verify_while(["111111", "222222", "333333"], "123456")
    print("FOR LOOP - lock, blank does not count")
    verify_for(["", "111111", "222222", "333333"], "123456")
    print("EXTRA ATTEMPTS")
    verify_with_security(["111111", "222222", "333333", "123456"], "123456", True)
    loop_control_demo()

if __name__ == "__main__":
    main()
