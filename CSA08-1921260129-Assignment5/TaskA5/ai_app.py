import re
import sqlite3
from collections import Counter

POSITIVE = {"good", "clean", "fast", "helpful", "improved", "safe", "better", "excellent", "fresh", "healthy"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken", "unsafe", "worse", "poor", "harmful"}
NEGATORS = {"not", "never", "no", "hardly"}
STOP_WORDS = {"the", "a", "an", "is", "are", "was", "were", "and", "or", "of", "to", "in", "on", "for", "from", "it", "this", "that", "we", "i", "they", "our", "at", "with", "be", "very", "today"}


def tokens(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def score(text):
    words = tokens(text)
    total = 0
    for i, word in enumerate(words):
        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0
        if i and words[i - 1] in NEGATORS:
            value *= -1
        total += value
    return total


def label(text):
    value = score(text)
    return "positive" if value > 0 else "negative" if value < 0 else "neutral"


def summarize(text, k=2):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    if not sentences:
        return ""
    words = [w for w in tokens(text) if w not in STOP_WORDS]
    counts = Counter(words)
    ranked = []
    for index, sentence in enumerate(sentences):
        sentence_words = [w for w in tokens(sentence) if w not in STOP_WORDS]
        ranked.append((sum(counts[w] for w in sentence_words), -index, sentence))
    chosen = sorted(ranked, reverse=True)[:max(1, k)]
    chosen_indices = {item[1] for item in chosen}
    return " ".join(item[2] for item in sorted(chosen, key=lambda x: -x[1]))


def answer_question(question, db_path):
    match = re.search(r"pm\s*2\.5.*?in\s+([a-z][a-z ]+?)(?:\s+today|\?|$)", question.lower())
    if not match:
        return "Please ask: What is the PM2.5 in <station> today?"
    station = " ".join(match.group(1).split()).title()
    con = sqlite3.connect(db_path)
    try:
        day = con.execute("SELECT MAX(day) FROM readings").fetchone()[0]
        row = con.execute("""SELECT AVG(r.pm25) FROM readings r JOIN stations s USING(station_id)
                              WHERE s.station_name=? AND r.day=?""", (station, day)).fetchone()
    finally:
        con.close()
    if not row or row[0] is None:
        return f"No PM2.5 reading is available for {station} on the latest data date."
    return f"Latest available PM2.5 for {station} on {day} is {row[0]:.1f} µg/m³."


def main():
    examples = ["Roads are clean and the bus was fast.", "Smoke from the factory, air is bad.",
                "The staff were not helpful.", "Not bad, service improved."]
    for sentence in examples:
        print(f"{label(sentence):8} | {sentence}")
    complaint = "The air is not clean, but the bus service is fast."
    print("Summary:", summarize(complaint, 1))


if __name__ == "__main__":
    main()
