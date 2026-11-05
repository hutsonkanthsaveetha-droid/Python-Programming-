# B2 - Adversarial data results

| Input | Observed behaviour | What it reveals |
|---|---|---|
| Missing `pm25` column | Rejected as an invalid header | Required schema must be validated before row processing |
| Semicolon delimiter | Sniffer detects `;` and reads the row | Do not assume a comma delimiter |
| Latin-1 text | UTF-8 decode fails; Latin-1 fallback reads the row | Encoding must be explicit and recoverable |
| Empty file | Reported as empty, with no parser crash | Empty inputs need a separate status |

The SQL-concatenation attack `Adyar' OR '1'='1` returns every row in the demonstration because it changes the WHERE condition. The parameterised `WHERE station = ?` treats the payload as data and returns no match.

The lexicon gives neutral to “Great, another day of toxic air” (sarcasm), “Not bad, not good either” (two negated terms cancel), “The service is good but the air is dirty” (mixed opinions cancel), and “I do not dislike the improvement” (words are outside the small lexicon). This identifies the limits of a one-token negation rule and fixed word list.
