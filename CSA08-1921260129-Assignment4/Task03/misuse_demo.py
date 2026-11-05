# Deliberate demonstration: a broad handler hides the misspelled name.
def hidden_typo():
    try:
        total = 10
        return totla + 5
    except Exception:
        pass


if __name__ == '__main__':
    print('Result:', hidden_typo())
    print('The NameError was swallowed, so the program printed None.')
