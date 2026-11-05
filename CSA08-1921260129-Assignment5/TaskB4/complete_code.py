POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}


def score(text):
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    for index, word in enumerate(words):
        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0
        if index > 0 and words[index - 1] in NEGATORS:
            value = -value
        total += value
    return total


def label(text):
    value = score(text)
    return "positive" if value > 0 else "negative" if value < 0 else "neutral"


for complaint in [
    "Roads are clean and the bus was fast.",
    "Smoke from the factory, air is bad.",
    "The staff were not helpful.",
    "Not bad, service improved.",
]:
    print(f"{label(complaint):8} | {complaint}")
